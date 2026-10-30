# The Listening Dark — website

The official site for **The Listening Dark** by **KP Cap** — an **adult
fantasy romance (romantasy)**, Book One of a new series.
Plain **HTML / CSS / JS** — no build tools, no framework, no dependencies to install.

> Concept: *a violet night sky under twin moons.* Moonlight text, gold-foil and
> Danaya-violet accents, a static starfield, and the book's own words doing the
> selling — the real back-cover copy, real quotes, real bio. Calm by design:
> no flicker, no grain, comfortable contrast throughout.

## Assets in place

| Asset | File | Used by |
|---|---|---|
| Cover art | `assets/cover.jpg` (900×1333) | Home story section, `book.html` |
| Author photo | `assets/author.jpg` (900×1350) | Home author section (arch crop), `author.html` portrait |
| OG share image | `assets/og.png` (1200×630) | `og:image` / `twitter:image` on every page |
| Twin-moon artwork | `assets/moons.webp` (1100×1100, 149 KB) | Home hero — **generated**, see below |
| Signed-copy poster | `assets/signed-copy.jpg` (900×1187) | Home `#signed` section |
| Favicons | `favicon.ico`, `favicon.svg`, `favicon-48.png`, `apple-touch-icon.png` (site root) | Every page — regenerate with `python tools/make_favicons.py` |

The cover is the front panel cropped out of the full hardcover spread
(`Downloads/The.png`, 5895×4240): the spine's right edge sits at x=3033, so the
panel is `crop((3033, 0, 5895, 4240))` scaled to 900px wide. The OG card is built
from that same JPG. Both are referenced with explicit `width`/`height`, so update
those attributes in `tools/build.py` whenever the artwork's proportions change —
and check the alt text still describes what is actually on the cover.

### The hero moons are generated, not stock

`python tools/make_moons.py` renders `assets/moons.webp` from scratch: the crater
field, the warm limb light and the smoke are all synthesised from seeded noise,
so the image is original artwork with no licensing question attached. Change
`SEED` at the top for a different moon; the composition stays put. Needs numpy,
scipy and Pillow — none of which the site itself depends on.

---

## Run it

**Just open `index.html` in a browser** (double-click it). That's the whole site.

For a nicer local experience (so fonts and links behave exactly like production),
serve the folder over http:

```bash
# from this folder — pick one:
python -m http.server 8000        # then visit http://localhost:8000
npx serve .                        # if you have Node
```

## Deploy it

Drag-and-drop the whole folder to any static host — no configuration needed
(signed-copy live values need server-side includes, so on a plain static host they
show their fallbacks):

- **Netlify** (drop the folder onto app.netlify.com) — auto-serves `404.html`.
- **Vercel**, **Cloudflare Pages**, **GitHub Pages** — all work as-is.

---

## Pages

| File | Page |
|---|---|
| `index.html` | Home — the full cinematic scroll |
| `book.html` | About the Book (synopsis, themes, details) |
| `author.html` | About the Author (bio, portrait, dedication) |
| `press.html` | Press Kit (emptied — placeholder until assets are approved) |
| `faq.html` | FAQ |
| `contact.html` | Contact |
| `privacy.html` · `terms.html` · `cookies.html` · `accessibility.html` | Legal |
| `404.html` | Not-found |
| `thank-you.html` · `checkout-unavailable.html` | Where checkout sends buyers after paying, and where a failed or full checkout lands. Only generated when `SHOP_ENABLED` is `True`; `noindex`, not in the sitemap |

## Structure

```
index.html …            all pages (plain HTML, edit directly)
css/style.css           the entire design system + components
js/main.js              all behaviour (nav, menu, reveals, forms)
assets/fonts/           Fraunces · Newsreader · Inter · Space Mono (local .woff2)
tools/build.py          optional generator — regenerates the HTML from shared
                        nav/footer fragments so they never drift. NOT required
                        to run the site.
tools/check_site.py     checks the shop-off and shop-on builds (see below)
tools/fixtures/shop/    sample include files used by check_site.py; do not edit by hand
tools/hooks/pre-commit  blocks secrets and order data from being committed
```

> **Editing tip:** the nav bar and footer are identical on every page. If you
> change them, **edit `tools/build.py` and re-run `python tools/build.py`** —
> treat the HTML files as generated output. (Hand-edits to the HTML will be
> silently overwritten the next time the generator runs.)

### One-time setup per clone

The repo is public, so enable the pre-commit hook before your first commit:

```bash
git config core.hooksPath tools/hooks
```

It refuses commits that contain Stripe key patterns, private keys, `.env` files,
database or `.csv` files, or `DEPLOY.local.md`. `git config core.hooksPath`
should then print `tools/hooks`.

### Build settings

Everything that changes between releases is a constant at the top of
`tools/build.py`. Change it, run `python tools/build.py`, commit the regenerated
HTML, deploy.

| Constant | What it does |
|---|---|
| `KINDLE_URL` | Every Kindle button |
| `PAPERBACK_URL` | The Amazon paperback button, Formats row and FAQ link. The store service carries the same URL in `src/fragments.js` and the two must match |
| `PUB_DATE`, `PUB_DATE_ISO` | Publication date shown on the site and in the JSON-LD |
| `PRE_ORDER` | `True` says "Pre-order on Kindle"; set `False` on release day |
| `SHOP_ENABLED` | The author's sign-off for the signed-copy shop. `False` (the default) builds the site with no signed-copy sales machinery. `True` adds the include points, the signed-copy sections of the terms, privacy and cookie pages, `thank-you.html` and `checkout-unavailable.html` |
| `PRICE_USD` | e.g. `"22.00"`. Used for fallbacks and the poster's alt text. The service that takes the orders owns the real price, and the two must match; the poster image has $22 printed on it |
| `SIGNED_SHIPS` | Ship window, e.g. `"within 14 days"`. Printed in the terms and the thank-you page, so it has to read correctly in a sentence. The service has its own copy of the same promise; change both together |
| `RETENTION` | How long order records are kept, worded for the privacy page |

**How live values arrive.** The signed-copy details that change (price line, copies
left, the order button, the refund policy in force, the signed edition in the
structured data) are not in the HTML. When `SHOP_ENABLED` is `True`, the build wraps
each of eight places in a server-side include (`ssi()` in `tools/build.py`) that the
web server fills from small files written by a separate service. Each include carries
a fallback inside the page. If the service is down, a file is missing or empty, or the
page is opened straight from disk or a plain static host, the fallback shows: the
signed-copy area reads "check back soon" and the rest of the page is unaffected. A
local preview therefore always shows fallbacks. Live values need a web server with
includes (SSI) enabled; the service and its setup are in a separate private
repository.

The build stops with an error rather than publish a bad state: an `ssi()` name that is
not one of the eight known fragments.

If the build prints `removed thank-you.html`, `removed checkout-unavailable.html` or
`removed commerce-disclosure.html`, a page from an earlier build was deleted: commit
the deletion, or the deploy leaves the old page online. (`commerce-disclosure.html`
no longer exists and is always removed.)

### Checking a build

```bash
python tools/check_site.py          # builds five scenarios in temp folders and checks each
python tools/check_site.py --keep   # same, and keeps the temp builds to inspect
```

It never touches the HTML in the repo. The scenarios are: shop off, shop on
(structure), includes emulated with their fallbacks (must equal the shop-off pages),
includes emulated with the sample files in `tools/fixtures/shop/` (open, sold out,
closed), and build guards. A good run ends with `89 passed, 0 failed` and exits 0;
any `[FAIL]` line names the scenario and the check. If the fixtures folder is missing
the fourth scenario prints `[SKIP]` and the total is lower. Run it before every build
that touches signed-copy code. The sample files are generated by the service
(`npm run fixtures` there) and copied in; regenerate them when its output changes.

---

## Before launch — what's left

Real content is now live: the official back-cover synopsis, quotes, author bio,
dedication, socials (@kpcapitulo / @kp.capitulo), genre & content notes.
Still to do:

- **Book details** as they firm up (formats, page count, ISBN, publication date)
- **Press kit downloads** (currently "coming soon" cards)
- **Legal copy** (drafts in place — review with counsel)
- **Signed copies**: the site side is built and switched off (`SHOP_ENABLED = False`);
  going live needs the separate service running and the author's approval

## The forms

Both the waitlist and the contact form POST via **FormSubmit AJAX** to the address
in `ENDPOINT` at the top of the form section in `js/main.js`. They validate inline,
show sending/error states, and carry a honeypot field.

**One action is still required:** FormSubmit emails a one-time activation link to
that inbox on the first real submission. Until someone clicks it, nothing is
delivered. Swap to Kit or Beehiiv later if a managed list with unsubscribe is wanted.

---

## Design notes

- **Deliberately dark-only** — a committed nocturnal world; the theme toggle is intentionally ignored.
- **Every quote on the site is verbatim from the manuscript**, and cited to the
  character who says it. Marketing copy (the synopsis, the spec strips) is
  clearly framed as description, never set in quotation marks as if it were the
  book's prose. Check any new pull-quote against `The_Listening_Dark_BETA.docx`
  before it ships — two lines that had been on the home page were blurb copy
  that appears nowhere in the book.
- **The home page follows the Sept 2026 redesign comps** (`listening-dark-home-handoff`):
  stacked hero title under twin moons, staged cover, soft ask, full-bleed pull-quote,
  arch-cropped author portrait. Buttons and text links are sentence case site-wide;
  uppercase tracking is reserved for kickers and meta.
- **Accessible** — keyboard-navigable, visible focus, honours `prefers-reduced-motion`
  (reveals switch off), semantic structure.
- **Fast** — fonts are local & subset; no external requests; works offline.
- Full design rationale lives in the approved design plan.
