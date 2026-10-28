#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checks the shop-off and shop-on builds against the fragment contract (payments-plan/12).
Each scenario builds a patched copy of tools/build.py in a temp dir, so the repo's HTML is never touched.
Run:  python tools/check_site.py [--keep]
"""
import glob, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_PY = os.path.join(HERE, "build.py")
FIXTURES = os.path.join(HERE, "fixtures", "shop")
KEEP = "--keep" in sys.argv

EXISTING = ["index", "book", "author", "press", "faq", "contact", "privacy",
            "terms", "cookies", "accessibility", "404"]
SHOP_PAGES = ("thank-you.html", "checkout-unavailable.html")
# the shop legitimately rewrites these, so they are left out of the golden comparison
SHOP_CHANGES = ("privacy.html", "terms.html", "cookies.html") + SHOP_PAGES
PLACEHOLDER_RE = re.compile(r"\{[A-Z_]+\}")

NAMES = ("ld-signed", "hero-cta", "signed-spec", "signed-cta", "book-formats",
         "faq-signed", "terms-price", "terms-refund")
EXPECTED = {"index.html": ("ld-signed", "hero-cta", "signed-spec", "signed-cta"),
            "book.html": ("ld-signed", "book-formats"),
            "faq.html": ("faq-signed",),
            "terms.html": ("terms-price", "terms-refund")}
STATES = ("open", "soldout", "closed")

DIRECTIVE_RE = re.compile(r"<!--#.*?-->", re.S)
BLOCK_RE = re.compile(r'<!--# block name="([a-z-]+)" -->')
END_RE = re.compile(r"<!--# endblock -->")
INCLUDE_RE = re.compile(r'<!--# include virtual="/_shop/([a-z-]+)\.html" stub="([a-z-]+)" -->')
LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)

PILL = '<span class="btn btn-ghost btn-soon">Signed author&rsquo;s copy &middot; check back soon</span>'
TERMS_PRICE_FALLBACK = ("<p><strong>Price and payment.</strong> Signed copies cost $22.00 USD per copy; shipping is shown on "
                        "the order page and at checkout. Payment is in full at checkout through Stripe. Your order is "
                        "accepted when payment completes and you receive a receipt.</p>")
TERMS_REFUND_FALLBACK = ("<p><strong>Cancellations, returns and refunds.</strong> The refund policy for your order is the one "
                         "shown at checkout and in your receipt. A copy that arrives damaged, or is lost in the mail, is "
                         "always replaced or refunded.</p>")
REFUNDABLE = ("Cancel any time before your copy ships for a full refund. Because each copy is signed, we can&rsquo;t accept "
              "returns after shipping, except: if your copy arrives damaged, or is lost in the mail, we&rsquo;ll replace it "
              "or refund you in full. Tell us within 14 days of delivery (with a photo, if damaged). Refunds go back to the "
              "original payment method.")
FORM_OPEN = '<form class="signed-form" method="post" action="/api/checkout">'
FORMATS = {"open": "Kindle eBook &middot; Signed paperback (limited)",
           "soldout": "Kindle eBook &middot; Signed paperback (sold out)",
           "closed": "Kindle eBook"}
CONFIRM_CLAIMS = ("payment is confirmed", "payment confirmed", "payment was successful", "payment received",
                  "order is confirmed", "order confirmed")

results = []


def check(scenario, name, ok, why=""):
    results.append((scenario, name, bool(ok), why))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f" -- {why}"))


def build(overrides, pre_existing=(), patches=()):
    """Builds a patched copy; returns (returncode, outdir, missing constants/patches, output)."""
    out = tempfile.mkdtemp(prefix="tld-check-")
    os.makedirs(os.path.join(out, "tools"))
    with open(BUILD_PY, encoding="utf-8") as f:
        src = f.read()
    missing = []
    for name, value in overrides.items():
        # (?!=) so a top-level comparison line is never mistaken for the assignment
        pat = re.compile(r"^%s[ \t]*=(?!=).*$" % re.escape(name), re.M)
        src, n = pat.subn(lambda m: f"{name} = {value!r}", src, count=1)
        if not n:
            missing.append(name)
    for old, new in patches:
        if old not in src:
            missing.append(repr(old))
        src = src.replace(old, new, 1)
    with open(os.path.join(out, "tools", "build.py"), "w", encoding="utf-8") as f:
        f.write(src)
    for fn in pre_existing:
        with open(os.path.join(out, fn), "w", encoding="utf-8") as f:
            f.write("<html>stale</html>")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, os.path.join(out, "tools", "build.py")], cwd=out,
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=env, timeout=120)
    return p.returncode, out, missing, (p.stdout + p.stderr).strip()


def read(path_or_out, fn=None):
    path = os.path.join(path_or_out, fn) if fn else path_or_out
    if not os.path.exists(path):
        return ""
    # newline="" so the byte-for-byte comparison sees exactly what was written
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def html_files(out):
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(out, "*.html")))


def between(text, start, end):
    """Slice from the first `start` to the next `end` after it; '' if start is absent."""
    i = text.find(start)
    if i < 0:
        return ""
    j = text.find(end, i + len(start))
    return text[i:] if j < 0 else text[i:j]


def footer(html):
    return between(html, "<footer", "</footer>")


def head_of(html):
    return between(html, "<head>", "</head>")


def hero_cta(index):
    return between(index, 'class="hero-cta"', "</div>")


def signed_section(index):
    return between(index, 'id="signed"', "</section>")


def ld_blocks(html):
    """Every JSON-LD block, parsed; None for one that does not parse."""
    blocks = []
    for raw in LD_RE.findall(html):
        try:
            blocks.append(json.loads(raw))
        except ValueError:
            blocks.append(None)
    return blocks


def is_signed_ld(ld):
    return isinstance(ld, dict) and "signed" in str(ld.get("name", "")).lower()


def first_diff(a, b):
    i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
    return f"differs at char {i}: {a[max(0, i - 40):i + 60]!r} vs {b[max(0, i - 40):i + 60]!r}"


def emulate_ssi(html, fragments=None):
    """Mimics nginx ssi: a block is captured and dropped in place; an include prints its
    fragment when one is given and non-empty, otherwise the captured stub block."""
    fragments = fragments or {}
    blocks, out, pos, open_name, open_at = {}, [], 0, None, 0
    for m in DIRECTIVE_RE.finditer(html):
        tok = m.group(0)
        if open_name is None:
            out.append(html[pos:m.start()])
        if BLOCK_RE.fullmatch(tok):
            if open_name is not None:
                raise ValueError(f"nested block at {m.start()}")
            open_name, open_at = BLOCK_RE.fullmatch(tok).group(1), m.end()
        elif END_RE.fullmatch(tok):
            if open_name is None:
                raise ValueError(f"endblock without block at {m.start()}")
            blocks[open_name] = html[open_at:m.start()]
            open_name = None
        elif INCLUDE_RE.fullmatch(tok):
            if open_name is not None:
                raise ValueError(f"include inside block at {m.start()}")
            name, stub = INCLUDE_RE.fullmatch(tok).groups()
            frag = fragments.get(name)
            if frag:
                out.append(frag)
            elif stub in blocks:
                out.append(blocks[stub])
            else:
                raise ValueError(f"include {name} has no stub block {stub!r} before it")
        else:
            raise ValueError(f"unknown directive {tok!r}")
        pos = m.end()
    if open_name is not None:
        raise ValueError(f"unclosed block {open_name}")
    out.append(html[pos:])
    return "".join(out)


def directive_problems(fn, html):
    """Grammar, contract names, stub-before-include, balance, no nesting, nothing inside a tag."""
    probs = []
    toks = list(DIRECTIVE_RE.finditer(html))
    if html.count("<!--#") != len(toks):
        probs.append(f"{fn}: unterminated directive")
    defined, open_name = set(), None
    for m in toks:
        tok = m.group(0)
        b, e, i = BLOCK_RE.fullmatch(tok), END_RE.fullmatch(tok), INCLUDE_RE.fullmatch(tok)
        if b:
            if b.group(1) not in NAMES:
                probs.append(f"{fn}: block name {b.group(1)} not in contract")
            if open_name is not None:
                probs.append(f"{fn}: block {b.group(1)} nested in {open_name}")
            open_name = b.group(1)
        elif e:
            if open_name is None:
                probs.append(f"{fn}: stray endblock")
            else:
                defined.add(open_name)
            open_name = None
        elif i:
            name, stub = i.groups()
            if name not in NAMES:
                probs.append(f"{fn}: include {name} not in contract")
            if open_name is not None:
                probs.append(f"{fn}: include {name} inside block {open_name}")
            if stub != name or stub not in defined:
                probs.append(f"{fn}: include {name} stub={stub} has no earlier block of that name")
        else:
            probs.append(f"{fn}: bad directive {tok!r}")
    if open_name is not None:
        probs.append(f"{fn}: unclosed block {open_name}")
    # a directive inside an attribute value cuts the tag short at its own "-->"
    for tag in re.findall(r"<[a-zA-Z][^>]*>", html):
        if "<!--#" in tag:
            probs.append(f"{fn}: directive inside a tag: {tag[:80]!r}")
    return probs


def start(scenario, overrides, pre_existing=(), patches=()):
    print(f"\n{scenario}")
    rc, out, missing, log = build(overrides, pre_existing, patches)
    if missing:
        check(scenario, "patch targets exist in build.py", False, "not found: " + ", ".join(missing))
    return rc, out, log


def common_invariants(sc, out):
    hits = []
    for fn in html_files(out) + ["sitemap.xml", "robots.txt"]:
        text = read(out, fn)
        if "SHOPIFY" in text:
            hits.append(fn + ": SHOPIFY")
        if "buy.stripe.com" in text:
            hits.append(fn + ": buy.stripe.com")
        if "commerce-disclosure" in text:
            hits.append(fn + ": commerce-disclosure")
        for m in PLACEHOLDER_RE.findall(text):
            hits.append(f"{fn}: {m}")
    check(sc, "no SHOPIFY, buy.stripe.com, commerce-disclosure or {PLACEHOLDER} anywhere", not hits, "; ".join(hits[:5]))
    missing = [p for p in EXISTING if not os.path.exists(os.path.join(out, p + ".html"))]
    check(sc, "the 11 existing pages are generated", not missing, "missing: " + ", ".join(missing))
    check(sc, "commerce-disclosure.html not generated",
          not os.path.exists(os.path.join(out, "commerce-disclosure.html")), "file exists")
    sitemap = read(out, "sitemap.xml")
    bad = [s for s in ("404", "thank-you", "checkout-unavailable") if s in sitemap]
    check(sc, "sitemap has no 404, thank-you or checkout-unavailable", not bad, "found: " + ", ".join(bad))


def s1_default():
    sc = "S1 shop off (default)"
    rc, out, log = start(sc, {"SHOP_ENABLED": False})
    check(sc, "build exits 0", rc == 0, log[-300:])
    with_ssi = [fn for fn in html_files(out) if "<!--#" in read(out, fn)]
    check(sc, "no <!--# anywhere", not with_ssi, "found in: " + ", ".join(with_ssi))
    for fn in SHOP_PAGES:
        check(sc, f"{fn} not generated", not os.path.exists(os.path.join(out, fn)), "file exists")
    api = [fn for fn in html_files(out) if "/api/checkout" in read(out, fn)]
    check(sc, "no /api/checkout anywhere", not api, "found in: " + ", ".join(api))
    linked = [fn for fn in html_files(out) if "commerce-disclosure" in footer(read(out, fn))]
    check(sc, "no footer links to commerce-disclosure", not linked, "linked from: " + ", ".join(linked))
    index = read(out, "index.html")
    check(sc, "closed pill inside the hero", PILL in hero_cta(index), "no pill in .hero-cta")
    check(sc, "closed pill inside #signed", PILL in signed_section(index), "no pill in #signed")
    check(sc, "privacy does not name Stripe", "Stripe" not in read(out, "privacy.html"), "Stripe found")
    check(sc, "terms has no Signed copies section",
          not re.search(r"<h2[^>]*>\s*Signed copies", read(out, "terms.html")), "h2 present")
    common_invariants(sc, out)
    return out


def s2_shop_on():
    sc = "S2 shop on, structure"
    rc, out, log = start(sc, {"SHOP_ENABLED": True})
    check(sc, "build exits 0", rc == 0, log[-300:])
    misplaced = []
    for fn in html_files(out):
        html = read(out, fn)
        want = EXPECTED.get(fn, ())
        for name in NAMES:
            inc = len(re.findall(r'<!--# include virtual="/_shop/%s\.html"' % re.escape(name), html))
            blk = html.count(f'<!--# block name="{name}" -->')
            n = 1 if name in want else 0
            if inc != n or blk != n:
                misplaced.append(f"{fn}: {name} include x{inc} block x{blk}, want x{n}")
    check(sc, "each include and block appears exactly once on exactly its page(s)", not misplaced,
          "; ".join(misplaced[:5]))
    probs = [p for fn in html_files(out) for p in directive_problems(fn, read(out, fn))]
    check(sc, "directives match the grammar, contract names, stub-before-include, balanced, not in tags",
          not probs, "; ".join(probs[:5]))
    for fn in ("index.html", "book.html"):
        check(sc, f"{fn} ld-signed include sits inside <head>",
              '<!--# include virtual="/_shop/ld-signed.html"' in head_of(read(out, fn)), "not in head")

    sitemap = read(out, "sitemap.xml")
    for fn in SHOP_PAGES:
        page = read(out, fn)
        check(sc, f"{fn} generated", page, "file missing")
        check(sc, f"{fn} has robots noindex", '<meta name="robots" content="noindex">' in page, "no noindex meta")
        check(sc, f"{fn} has no canonical", page and 'rel="canonical"' not in page,
              "canonical present" if page else "file missing")
        check(sc, f"{fn} not in sitemap", fn not in sitemap, "in sitemap.xml")
        low = page.lower()
        claims = [c for c in CONFIRM_CLAIMS if c in low]
        check(sc, f"{fn} never claims payment is confirmed", page and not claims,
              f"found {claims}" if page else "file missing")
    check(sc, "checkout-unavailable says nothing was charged",
          "nothing was charged" in read(out, "checkout-unavailable.html").lower(), "no such sentence")

    privacy = read(out, "privacy.html")
    low = privacy.lower()
    check(sc, "privacy names Stripe", "Stripe" in privacy, "no Stripe")
    check(sc, "privacy no longer says 'no payments'", "no payments" not in privacy, "still says it")
    check(sc, "privacy mentions no phone number", "phone" not in low, "phone found")
    check(sc, "privacy mentions no inscription", "inscri" not in low, "inscription found")
    check(sc, "privacy says she ships via the military postal service", "military postal service" in privacy, "missing")
    terms = read(out, "terms.html")
    check(sc, "terms has a Signed copies section", re.search(r"<h2[^>]*>\s*Signed copies", terms), "no h2")
    check(sc, "terms has a Limited stock paragraph", "<p><strong>Limited stock.</strong>" in terms, "missing")
    ship = between(terms, "<p><strong>Shipping.</strong>", "</p>")
    for want in ("within 14 days", "APO/FPO/DPO", "military post office"):
        check(sc, f"terms Shipping paragraph mentions {want!r}", want in ship,
              "no Shipping paragraph" if not ship else "not found")
    check(sc, "terms no longer says 'informational site'", "informational site" not in terms, "still says it")
    cookies = read(out, "cookies.html")
    check(sc, "cookies still says 'sets no cookies'", "sets no cookies" in cookies, "missing")
    check(sc, "cookies mentions Stripe", "Stripe" in cookies, "no Stripe")
    common_invariants(sc, out)
    return out


def s3_stubs(off, on):
    sc = "S3 SSI emulation with stubs (fallbacks == shop-off site)"
    print(f"\n{sc}")
    want = set(html_files(off))
    got = set(html_files(on)) - set(SHOP_PAGES)
    check(sc, "shop-on builds the same page set plus the two shop pages", want == got,
          f"only off: {sorted(want - got)}, only on: {sorted(got - want)}")
    for fn in sorted(want & got):
        if fn in SHOP_CHANGES:
            continue
        try:
            em = emulate_ssi(read(on, fn))
        except ValueError as e:
            check(sc, f"{fn} emulated == shop-off", False, f"emulator: {e}")
            continue
        ref = read(off, fn)
        check(sc, f"{fn} emulated == shop-off byte for byte", em == ref, first_diff(em, ref))
    try:
        terms = emulate_ssi(read(on, "terms.html"))
        index = emulate_ssi(read(on, "index.html"))
    except ValueError as e:
        check(sc, "terms and index emulate", False, f"emulator: {e}")
        return
    check(sc, "emulated terms shows the price fallback", TERMS_PRICE_FALLBACK in terms, "missing")
    check(sc, "emulated terms shows the refund fallback", TERMS_REFUND_FALLBACK in terms, "missing")
    lds = ld_blocks(index)
    check(sc, "emulated index JSON-LD parses", lds and None not in lds, f"blocks: {lds}")
    check(sc, "emulated index JSON-LD has no signed edition", not any(is_signed_ld(x) for x in lds), "signed block found")


def s4_fixtures(on):
    sc = "S4 SSI emulation with fixtures"
    print(f"\n{sc}")
    if not all(os.path.isdir(os.path.join(FIXTURES, s)) for s in STATES):
        print("\n" + "=" * 72)
        print("[SKIP] S4 fixtures not present (run npm run fixtures in store)")
        print("=" * 72)
        return
    pages = {fn: read(on, fn) for fn in ("index.html", "book.html", "terms.html")}
    for state in STATES:
        frags = {n: read(os.path.join(FIXTURES, state, n + ".html")) for n in NAMES}
        empty = [n for n, v in frags.items() if not v.strip()]
        check(sc, f"{state}: all 8 fixture files exist and are non-empty", not empty, "missing/empty: " + ", ".join(empty))
        try:
            em = {fn: emulate_ssi(html, frags) for fn, html in pages.items()}
        except ValueError as e:
            check(sc, f"{state}: pages emulate", False, f"emulator: {e}")
            continue
        index, signed, hero = em["index.html"], signed_section(em["index.html"]), hero_cta(em["index.html"])
        ld_raw = between(frags["ld-signed"], '<script type="application/ld+json">', "</script>")
        ld_raw = ld_raw[len('<script type="application/ld+json">'):]
        signed_lds = [x for x in ld_blocks(index) if is_signed_ld(x)]
        offer = (signed_lds[0] if signed_lds else {}).get("offers") or {}
        formats = between(em["book.html"], "<dt>Formats</dt><dd>", "</dd>")[len("<dt>Formats</dt><dd>"):].strip()
        check(sc, f"{state}: book Formats row reads {FORMATS[state]!r}", formats == FORMATS[state], f"row: {formats!r}")
        if state == "open":
            check(sc, "open: exactly one checkout form", index.count(FORM_OPEN) == 1, f"{index.count(FORM_OPEN)} found")
            form = between(index, FORM_OPEN, "</form>")
            label = re.search(r'<button\b[^>]*type="submit"[^>]*>(.*?)</button>', form, re.S)
            check(sc, "open: submit label contains $22", label and "$22" in label.group(1), "no $22 submit")
            check(sc, "open: hero links to #signed", 'href="#signed"' in hero, "no href=#signed")
            spec = between(signed, '<dl class="spec spec-ruled reveal">', "</dl>")
            rows = len(re.findall(r"<div><dt>.*?</dt><dd>.*?</dd></div>", spec, re.S))
            check(sc, "open: signed-spec has 4 rows", rows == 4, f"{rows} rows")
            check(sc, "open: ld-signed parses, 22.00 InStock",
                  len(signed_lds) == 1 and offer.get("price") == "22.00"
                  and str(offer.get("availability", "")).endswith("InStock"), f"offer: {offer or 'missing'}")
            check(sc, "open: ld-signed JSON has no raw <", ld_raw and "<" not in ld_raw, "raw < or no script")
            check(sc, "open: terms shows the refundable policy", REFUNDABLE in em["terms.html"], "missing")
        elif state == "soldout":
            check(sc, "soldout: no checkout form", "<form class=\"signed-form\"" not in index, "form present")
            check(sc, "soldout: #signed says sold out", "sold out" in signed.lower(), "no 'sold out'")
            # the contract's soldout fragment is a comment that itself says "signed", so judge visible markup only
            visible = re.sub(r"<!--.*?-->", "", hero, flags=re.S)
            check(sc, "soldout: hero has no signed button", hero and "signed" not in visible.lower(), "signed text in hero")
            check(sc, "soldout: ld-signed parses, SoldOut",
                  len(signed_lds) == 1 and str(offer.get("availability", "")).endswith("SoldOut"),
                  f"offer: {offer or 'missing'}")
        else:
            check(sc, "closed: closed pill in hero and #signed", PILL in hero and PILL in signed, "pill missing")
            frag = frags["ld-signed"].strip()
            check(sc, "closed: ld-signed is a comment", frag.startswith("<!--") and frag.endswith("-->") and not signed_lds,
                  f"fragment: {frag[:60]!r}")


def s5_guards():
    sc = "S5 build guards"
    outs = []
    rc, out, log = start(sc, {"SHOP_ENABLED": True}, patches=[('ssi("hero-cta"', 'ssi("hero-ctx"')])
    outs.append(out)
    check(sc, "unknown fragment name fails the build", rc != 0 and "hero-ctx" in log, f"rc={rc}: {log[-200:]}")

    stale = ("commerce-disclosure.html",) + SHOP_PAGES
    rc, out, _, log = build({"SHOP_ENABLED": False}, pre_existing=stale)
    outs.append(out)
    check(sc, "shop off with stale files builds", rc == 0, log[-300:])
    for fn in stale:
        check(sc, f"shop off removes stale {fn}", not os.path.exists(os.path.join(out, fn)), "still present")
    check(sc, "shop off prints 'commit the deletion'", log.count("commit the deletion") == len(stale),
          f"{log.count('commit the deletion')} notices")

    rc, out, _, log = build({"SHOP_ENABLED": True}, pre_existing=stale)
    outs.append(out)
    check(sc, "shop on with stale files builds", rc == 0, log[-300:])
    check(sc, "shop on still removes commerce-disclosure.html",
          not os.path.exists(os.path.join(out, "commerce-disclosure.html")), "still present")
    for fn in SHOP_PAGES:
        page = read(out, fn)
        check(sc, f"shop on keeps a freshly built {fn}", page and "stale" not in page, "missing or still stale")
    return outs


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    outs, off, on = [], None, None

    def run(fn, *args):
        try:
            return fn(*args)
        except Exception as e:  # one broken scenario must not hide the rest
            check(fn.__name__, "scenario ran", False, f"{type(e).__name__}: {e}")
            return None

    off = run(s1_default)
    on = run(s2_shop_on)
    outs += [d for d in (off, on) if d]
    if off and on:
        run(s3_stubs, off, on)
    if on:
        run(s4_fixtures, on)
    outs += run(s5_guards) or []

    failed = [r for r in results if not r[2]]
    print(f"\n{len(results) - len(failed)} passed, {len(failed)} failed")
    if KEEP:
        print("kept build dirs:\n  " + "\n  ".join(outs))
    else:
        for d in outs:
            shutil.rmtree(d, ignore_errors=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
