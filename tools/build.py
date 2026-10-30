#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site generator for THE LISTENING DARK by KP Cap.
An adult fantasy romance (romantasy) — Book One of a new series.

Emits plain HTML files into the project root from shared fragments,
so the nav/footer stay identical across every page.
Run:  python tools/build.py
Output is standard HTML/CSS/JS — no runtime dependency on this script.

Synopsis, quotes and author bio are taken from the author's own
back-cover copy and manuscript (this is the author's site).
"""
import os, sys, datetime

SITE = "https://kpcapitulo.com"
KINDLE_URL = "https://a.co/d/0e4UUKSl"
PAPERBACK_URL = "https://a.co/d/07Q7zBZF"

# ---- Signed copies (plan: payments-plan/12; live values come from the store service) ----
# her sign-off: off builds today's site exactly, on adds the ssi include points and the sale terms
SHOP_ENABLED = True
# fallbacks and alt text only; the service owns the live price and must match it
PRICE_USD = "22.00"
SIGNED_SHIPS = "within 14 days"
RETENTION = "for as long as tax law requires us to keep business records"

PUB_DATE = "October 30, 2026"
PUB_DATE_ISO = "2026-10-30"
# release day: set False, rebuild, deploy
PRE_ORDER = False
BUY_LABEL = "Pre-order on Kindle" if PRE_ORDER else "Buy on Kindle"
AVAIL = "available to pre-order now" if PRE_ORDER else "out now"

PRICE = "$" + PRICE_USD.removesuffix(".00")
# must match the fragment files the service writes (payments-plan/12)
SSI_NAMES = ("ld-signed", "hero-cta", "signed-spec", "signed-cta", "book-formats", "faq-signed", "terms-price", "terms-refund", "nav-signed", "book-buy")

def ssi(name, fallback):
    if name not in SSI_NAMES:
        sys.exit(f"unknown ssi fragment: {name}")
    if not SHOP_ENABLED:
        return fallback
    # without ssi (local preview) both directives are comments and the fallback shows once
    return f'<!--# block name="{name}" -->{fallback}<!--# endblock --><!--# include virtual="/_shop/{name}.html" stub="{name}" -->'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YEAR = datetime.date.today().year

# ---- The twin-moon mark (Twin Moon Rite) — nav / footer ----
MARK = """<svg class="mark" viewBox="0 0 32 32" fill="none" aria-hidden="true"><circle cx="13" cy="14" r="8.5" stroke="#A78FE3" stroke-width="1.3" opacity=".9"/><circle cx="21.5" cy="20" r="5" fill="#D2A85E" opacity=".95"/><circle cx="25" cy="7.5" r="1.1" fill="#E6E3F2"/></svg>"""

# small mark for cover / empty states
MOON_SM = """<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" width="40" height="40"><circle cx="13" cy="14" r="8.5" stroke="#A78FE3" stroke-width="1.2" opacity=".9"/><circle cx="21.5" cy="20" r="5" fill="#D2A85E" opacity=".95"/><circle cx="25" cy="7.5" r="1.1" fill="#E6E3F2"/></svg>"""

# ---- Hero starfield: fixed positions, sliced to the viewport (never animates) ----
_PALE = [(64,120,1,.5),(212,48,.8,.4),(340,210,1.2,.35),(498,86,.8,.5),(610,300,1,.3),
         (702,40,1.4,.6),(780,160,.8,.4),(900,96,1,.45),(1180,30,.8,.4),(1320,70,1.2,.5),
         (1392,240,.8,.4),(1360,420,.8,.35),(1400,610,1.4,.5),(1260,760,1,.35),
         (140,520,.8,.3),(40,700,1.2,.4),(280,400,.7,.3),(420,640,1,.25),
         (560,820,.8,.3),(720,520,.7,.3),(860,760,1,.4),(1010,840,.8,.35)]
_GOLD = [(836,232,1.6,.8),(1288,820,1.4,.7)]

def _stars(pts):
    return "".join('<circle cx="%s" cy="%s" r="%s" opacity="%s"/>' % pt for pt in pts)

HERO_STARS = ('<svg class="hero-stars" aria-hidden="true" viewBox="0 0 1440 880" '
              'preserveAspectRatio="xMidYMid slice">'
              '<g fill="#E6E3F2">' + _stars(_PALE) + '</g>'
              '<g fill="#D2A85E">' + _stars(_GOLD) + '</g></svg>')

STAR_4 = ('<svg class="star" aria-hidden="true" width="16" height="16" viewBox="0 0 16 16">'
          '<path d="M8 0 L9.2 6.8 L16 8 L9.2 9.2 L8 16 L6.8 9.2 L0 8 L6.8 6.8 Z" fill="currentColor"/></svg>')

DIV_STAR = """<div class="divider-star" aria-hidden="true"><span>&#10022;&nbsp;&nbsp;&#10022;</span></div>"""

def head(title, desc, url=None, extra=""):
    canon = f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n' if url else ""
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#141119">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Listening Dark">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/assets/og.png">
{canon}{extra}<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/fraunces.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/inter.woff2" crossorigin>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="sky" aria-hidden="true"></div>
"""

def kindle_btn(cls=""):
    return f'<a class="btn btn-primary{cls}" href="{KINDLE_URL}" target="_blank" rel="noopener">{BUY_LABEL}</a>'

SPEC_FALLBACK = '<dl class="spec spec-ruled reveal">\n            <div><dt>Price</dt><dd>$22 USD</dd></div>\n            <div><dt>Signed by</dt><dd>KP Capitulo</dd></div>\n            <div><dt>Shipping</dt><dd>USPS, US and APO/FPO/DPO</dd></div>\n            <div><dt>Availability</dt><dd>Limited quantity</dd></div>\n          </dl>'
# neutral on purpose: true before the first run and while she pauses sales
PILL = '<span class="btn btn-ghost btn-soon">Signed author&rsquo;s copy &middot; check back soon</span>'
# same markup the service writes while closed, so a down service reads like a closed shop
BUY_FALLBACK = '<div class="buy-opt buy-signed"><p class="buy-kicker">Signed author&rsquo;s copy</p><p class="buy-line">Opens soon.</p></div>'

def get_copy(cls):
    return f"""  <section class="{cls}" id="get">
    <div class="wrap">
      <div class="get-copy reveal">
        <p class="kicker k-gold">Get your copy</p>
        <div class="buy-pair">
          <div class="buy-opt"><p class="buy-kicker">Kindle eBook</p><p class="buy-line">The Kindle edition is {AVAIL}.</p>{kindle_btn()}</div>
          <div class="buy-opt"><p class="buy-kicker">Paperback</p><p class="buy-line">The paperback is out now on Amazon.</p><a class="btn btn-ghost" href="{PAPERBACK_URL}" target="_blank" rel="noopener">Buy the paperback</a></div>
          {ssi("book-buy", BUY_FALLBACK)}
        </div>
      </div>
    </div>
  </section>
"""

def nav(active):
    def link(href, label, key):
        cur = ' aria-current="page"' if key == active else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    links = "".join([
        link("book.html", "The Book", "book"),
        link("author.html", "The Author", "author"),
        link("press.html", "Press", "press"),
        link("faq.html", "FAQ", "faq"),
    ])
    return f"""<nav class="nav" aria-label="Primary">
  <div class="nav-in">
    <a class="brand" href="index.html" aria-label="The Listening Dark — home">{MARK}<span class="word">The Listening Dark</span></a>
    <div class="nav-links">
      {ssi("nav-signed", "")}{links}
      {kindle_btn(" btn-mini")}
    </div>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  </div>
</nav>
<div class="menu" id="menu" aria-hidden="true">
  <nav class="menu-links" aria-label="Mobile">
    <a href="index.html">Home</a>
    {ssi("nav-signed", "")}
    <a href="book.html">The Book</a>
    <a href="author.html">The Author</a>
    <a href="press.html">Press</a>
    <a href="faq.html">FAQ</a>
  </nav>
  <div class="menu-foot">
    {kindle_btn()}
    <div class="menu-social"><a href="https://instagram.com/kpcapitulo" rel="noopener">Instagram</a><a href="https://tiktok.com/@kp.capitulo" rel="noopener">TikTok</a><a href="contact.html">Contact</a></div>
  </div>
</div>
"""

# ---- The real cover art (cropped from the author's hardcover design) ----
def cover_block(large=False):
    cls = "cover cover-img lg" if large else "cover cover-img"
    return f"""<div class="cover-stage reveal">
          <div class="{cls}" id="cover">
            <img src="assets/cover.jpg" alt="The Listening Dark by KP Capitulo &mdash; front cover: twin moons, one eclipsing the other in a ring of gold light, rising through dark cloud" width="900" height="1333" loading="lazy">
          </div>
        </div>"""

def waitlist_section():
    """Secondary ask now Kindle is out: print editions and Book Two. Full-bleed,
    twin moons cropped by the section's top edge, visible field label."""
    return """  <section class="section waitlist" id="waitlist">
    <span class="wl-moon wl-moon-a" aria-hidden="true"></span>
    <span class="wl-moon wl-moon-b" aria-hidden="true"></span>
    <div class="wrap">
      <p class="kicker k-gold center reveal">The Invitation</p>
      <h2 class="reveal">Hold it in <em>your hands.</em></h2>
      <p class="lead reveal">The hardcover is on its way. Leave your email and we&rsquo;ll tell you the day it lands, along with first word on Book Two.</p>
      <form class="wl-form reveal" data-waitlist novalidate>
        <div class="hp" aria-hidden="true"><label>Leave blank<input type="text" tabindex="-1" autocomplete="off"></label></div>
        <label class="wl-label" for="wl-email">Email address</label>
        <div class="field">
          <input id="wl-email" type="email" autocomplete="email" placeholder="you@example.com" required>
          <button class="btn btn-primary" type="submit">Notify Me</button>
        </div>
      </form>
      <p class="form-msg" role="status" aria-live="polite"></p>
      <p class="wl-note">No noise. One message when it matters. Unsubscribe anytime.</p>
    </div>
  </section>
"""

def footer(wl_target):
    return f"""  <footer class="footer">
    <div class="wrap">
      <div class="foot-grid">
        <div class="foot-brand">
          {MARK}
          <div class="fw">The Listening Dark</div>
          <p>&ldquo;Magic is just the world paying attention to you.&rdquo;</p>
        </div>
        <div class="foot-col">
          <h4>Explore</h4>
          <a href="book.html">The Book</a><a href="author.html">The Author</a><a href="press.html">Press Kit</a>
        </div>
        <div class="foot-col">
          <h4>Connect</h4>
          <a href="{wl_target}">Get updates</a><a href="contact.html">Contact</a><a href="https://instagram.com/kpcapitulo" rel="noopener">Instagram</a><a href="https://tiktok.com/@kp.capitulo" rel="noopener">TikTok</a>
        </div>
        <div class="foot-col foot-mini">
          <h4>Print editions &amp; Book Two</h4>
          <p>One email when the hardcover lands. No noise.</p>
          <form data-waitlist novalidate>
            <div class="hp" aria-hidden="true"><label>Leave blank<input type="text" tabindex="-1" autocomplete="off"></label></div>
            <div class="field"><input id="ft-email" type="email" autocomplete="email" placeholder="you@email.com" aria-label="Email address" required><button class="btn btn-primary btn-mini" type="submit">Join</button></div>
            <p class="form-msg" role="status" aria-live="polite"></p>
          </form>
        </div>
      </div>
      <div class="foot-base">
        <span>&copy; <span data-year>{YEAR}</span> KP Cap &middot; All rights reserved</span>
        <div class="legal">
          <a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><a href="cookies.html">Cookies</a><a href="accessibility.html">Accessibility</a>
          <a class="to-top" href="#top">Back to top &uarr;</a>
        </div>
      </div>
    </div>
  </footer>
</main>
<script src="js/main.js"></script>
</body>
</html>
"""

PAGES = []

def page(filename, title, desc, active, body, wl_target="#waitlist", extra_head="", listed=True):
    url = None
    if listed:
        url = SITE + "/" + ("" if filename == "index.html" else filename)
        PAGES.append(url)
    html = head(title, desc, url, extra_head) + nav(active) + '<main class="content" id="main"><span id="top"></span>\n' + body + footer(wl_target)
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename, f"({len(html)} bytes)")

# =====================================================================
#  REAL CONTENT — from the manuscript
# =====================================================================

# =====================================================================
#  PAGE BODIES
# =====================================================================

HOME = f"""  <header class="hero">
    {HERO_STARS}
    <div class="hero-moons" aria-hidden="true">
      <img class="moon-art" src="assets/moons.webp" alt="" width="1100" height="1100" decoding="async" fetchpriority="high">
    </div>
    <div class="wrap hero-inner">
      <p class="kicker k-gold eyebrow" data-reveal>An Adult Fantasy Romance &middot; Book One &middot; KP&nbsp;Cap</p>
      <h1 class="hero-title" data-reveal>
        <span class="ht-the">The</span>
        <span class="ht-a">Listening</span>
        <span class="ht-b">Dark</span>
      </h1>
      <p class="hero-sub" data-reveal>I don&rsquo;t aim it. I don&rsquo;t need to. <em>It listens.</em></p>
      <div class="hero-cta" data-reveal>
        {kindle_btn()}
        {ssi("hero-cta", PILL)}
      </div>
    </div>
    <div class="wrap hero-foot" data-reveal>
      <span class="rule" aria-hidden="true"></span>
      <span class="pub">Publication &middot; {PUB_DATE}</span>
    </div>
  </header>

  <section class="section-sm premise">
    <div class="wrap">
      <div class="reveal">{STAR_4}</div>
      <p class="reveal">Some doors aren&rsquo;t locked. They&rsquo;re simply not for everyone.</p>
    </div>
  </section>

  <section class="section section-deep" id="book">
    <div class="wrap">
      <div class="story-grid">
        <div class="cover-staged reveal">
          <span class="cs-ring" aria-hidden="true"></span>
          <span class="cs-frame" aria-hidden="true"></span>
          <div class="cover cover-img">
            <img src="assets/cover.jpg" alt="The Listening Dark by KP Capitulo &mdash; front cover: twin moons, one eclipsing the other in a ring of gold light, rising through dark cloud" width="900" height="1333" loading="lazy">
          </div>
        </div>
        <div class="prose-head">
          <p class="kicker k-gold reveal">The Story</p>
          <h2 class="reveal">Camilla has always believed <em>she was human.</em></h2>
          <p class="kicker-note reveal">Until one morning, everything changes.</p>
          <div class="prose reveal">
            <p>A hidden power awakens within her, tearing apart the life she has always known and drawing her across a border she was never meant to cross.</p>
            <p class="prose-turn">Beyond it lies a world of ancient magic, powerful beings, and dragons &mdash; a world where nothing is as it seems, and where Camilla may be far more important than she ever imagined.</p>
          </div>
          <dl class="spec spec-ruled reveal">
            <div><dt>Genre</dt><dd>Adult Fantasy Romance</dd></div>
            <div><dt>Series</dt><dd>Book One</dd></div>
            <div><dt>Publication</dt><dd>{PUB_DATE}</dd></div>
          </dl>
          <p class="advisory reveal">18+ &middot; Contains explicit content, violence, and strong language.</p>
          <a class="link-txt reveal" href="book.html">More about the book <span class="arrow" aria-hidden="true">&rarr;</span></a>
        </div>
      </div>
    </div>
  </section>

{get_copy("section-xs section-deep")}
  <section class="section section-deep" id="signed">
    <div class="wrap">
      <div class="story-grid signed-grid">
        <figure class="signed-art reveal">
          <img src="assets/signed-copy.jpg" alt="Limited signed copy of The Listening Dark, 22 US dollars, personally signed by KP Capitulo, carefully packaged and shipped via USPS to US addresses only" width="900" height="1187" loading="lazy">
        </figure>
        <div class="prose-head">
          <p class="kicker k-gold reveal">Limited signed copy</p>
          <h2 class="reveal">A copy signed <em>by the author.</em></h2>
          {ssi("signed-spec", SPEC_FALLBACK)}
          <div class="signed-cta reveal">{ssi("signed-cta", PILL)}</div>
        </div>
      </div>
    </div>
  </section>

  <section class="quote-full">
    <span class="qf-ring qf-ring-a" aria-hidden="true"></span>
    <span class="qf-ring qf-ring-b" aria-hidden="true"></span>
    <div class="wrap">
      <span class="qf-mark" aria-hidden="true">&ldquo;</span>
      <blockquote class="reveal">My mother used to say magic is just the world paying attention to you. That some people the world notices more than others.</blockquote>
      <p class="qf-cite reveal">Dezi</p>
    </div>
  </section>

  <section class="section home-author" id="author">
    <div class="wrap">
      <div class="author-grid-home">
        <figure class="portrait-arch reveal">
          <span class="pa-frame" aria-hidden="true"></span>
          <img src="assets/author.jpg" alt="KP Cap, seated in a leather armchair in a reading nook lined with books" width="900" height="1350" loading="lazy">
        </figure>
        <div class="ha-body">
          <p class="kicker k-gold reveal">The Author</p>
          <h2 class="reveal">KP Cap</h2>
          <p class="ha-teaser reveal">A military spouse and a collector of random trinkets, KP Cap started this novel in 2017, rewrote it more times than she can count, and finished it during her baby&rsquo;s nap times. She has been dreaming up fantasy worlds since the sixth grade. <em>The Listening Dark</em> is her debut.</p>
          <div class="ha-links reveal">
            <a class="link-txt" href="author.html">Meet the author <span class="arrow" aria-hidden="true">&rarr;</span></a>
            <a href="https://instagram.com/kpcapitulo" rel="noopener">Instagram @kpcapitulo</a>
            <a href="https://tiktok.com/@kp.capitulo" rel="noopener">TikTok @kp.capitulo</a>
          </div>
        </div>
      </div>
    </div>
  </section>

{waitlist_section()}"""

# ---------- BOOK ----------
BOOK = f"""  <header class="page-hero">
    <div class="wrap">
      <div class="kicker center reveal">The Book</div>
      <h1 class="reveal">The Listening Dark</h1>
      <p class="lede reveal">Book One of a new adult romantasy series &mdash; dragons, found family, twin gods, and a power that refuses classification.</p>
    </div>
  </header>

  <section class="section-sm">
    <div class="wrap">
      <div class="book-grid">
        {cover_block(True)}
        <div class="prose-head">
          <div class="kicker reveal">The Story</div>
          <h2 class="reveal">Camilla has always believed <em>she was human.</em></h2>
          <div class="prose reveal">
            <p>Until one morning, everything changes.</p>
            <p>A hidden power awakens within her, tearing apart the life she has always known and drawing her across a border she was never meant to cross.</p>
            <p>Beyond it lies a world of ancient magic, powerful beings, and dragons &mdash; a world where nothing is as it seems, and where Camilla may be far more important than she ever imagined.</p>
            <p>As secrets unravel and forbidden connections begin to form, Camilla is forced to confront the truth about where she came from.</p>
            <p>And the more she learns, the more she realizes that the life she knew was only <em>the beginning.</em></p>
          </div>
        </div>
      </div>
    </div>
  </section>

{get_copy("section-xs")}
  <section class="section quote">
    <div class="wrap">
      {DIV_STAR}
      <blockquote class="reveal">&ldquo;Magic is not merely a force &mdash; it is a relationship. Between the self and the world. Between what exists and <em>what it reaches toward.</em>&rdquo;</blockquote>
      <cite class="reveal">From <em>The Listening Dark</em></cite>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="kicker center reveal" style="justify-content:center;margin-bottom:var(--s7)">The World</div>
      <div class="grid grid-3 stagger">
        <div class="card"><div class="card-num">01</div><h3>The Zidal</h3><p>A power you don&rsquo;t choose and can&rsquo;t study for. You&rsquo;re born with it, or you aren&rsquo;t &mdash; and training is how you learn to live with something that <em>already lives inside you.</em></p></div>
        <div class="card"><div class="card-num">02</div><h3>The Twin Moon Rite</h3><p>Once a year, when both moons rise together, potential riders enter the Orcaan. If a dragon chooses you, you&rsquo;re a rider. If not &mdash; <em>you get one chance. Ever.</em></p></div>
        <div class="card"><div class="card-num">03</div><h3>The Dragons</h3><p>Some are majestic. Some are vicious. Some are deeply strange. The rare ones don&rsquo;t choose riders by strength or bloodline &mdash; <em>they choose disruption.</em></p></div>
      </div>
    </div>
  </section>

  <section class="section-sm">
    <div class="wrap wrap-narrow">
      <div class="kicker reveal" style="margin-bottom:var(--s6)">The Details</div>
      <dl class="spec reveal" style="border-top:1px solid var(--line)">
        <div><dt>Genre</dt><dd>Adult Fantasy Romance</dd></div>
        <div><dt>Series</dt><dd>Book One</dd></div>
        <div><dt>Formats</dt><dd>{ssi("book-formats", "Kindle eBook &middot; <a href='" + PAPERBACK_URL + "' target='_blank' rel='noopener'>Paperback</a>")}</dd></div>
        <div><dt>Publication</dt><dd>{PUB_DATE}</dd></div>
        <div><dt>Audience</dt><dd>Adult &middot; 18+</dd></div>
      </dl>
      <div class="note reveal" style="margin-top:var(--s8)">
        <div class="kicker">Content Note</div>
        <p><em>The Listening Dark</em> is adult fantasy. It contains explicit content, violence, and language. Recommended for readers 18+.</p>
      </div>
    </div>
  </section>

{waitlist_section()}"""

# ---------- AUTHOR ----------
AUTHOR = f"""  <header class="page-hero">
    <div class="wrap">
      <div class="kicker center reveal">The Author</div>
      <h1 class="reveal">KP Capitulo</h1>
      <p class="lede reveal">Dreaming up fantasy worlds since the sixth grade. Writing this one since 2017.</p>
    </div>
  </header>

  <section class="section-sm">
    <div class="wrap">
      <div class="author-grid">
        <figure class="portrait reveal" style="margin:0">
          <img src="assets/author.jpg" alt="KP Capitulo, author of The Listening Dark, seated in a reading nook lined with books" width="900" height="1350" loading="lazy">
        </figure>
        <div class="author-bio">
          <div class="kicker reveal">Biography</div>
          <div class="prose reveal" style="margin-top:var(--s5)">
            <p><strong>KP Capitulo</strong> is a military spouse, a collector of random trinkets, and the kind of person who started writing a fantasy novel in 2017, rewrote it more times than she can count, and finally finished it during her baby&rsquo;s nap times &mdash; which, if you know newborns, makes this book an act of sheer determination.</p>
            <p>Born in the Netherlands and raised in the Philippines and now living wherever her husband goes, KP has been dreaming up fantasy worlds since the sixth grade, when a YA novel convinced her that magic was real and she should probably write some of her own.</p>
            <p>When she isn&rsquo;t building fictional realms, she&rsquo;s painting, drawing, chasing her three kids away from her laptop, or being emotionally supported by her cats and dog &mdash; who have heard every single draft of this book and have no notes.</p>
            <p><em>The Listening Dark</em> is her debut novel.</p>
          </div>
          <blockquote class="dedication reveal">For those whose minds are in the stars while their feet are on the ground &mdash; surviving the real world, and loving it anyway.</blockquote>
          <div class="social-row reveal">
            <a href="https://instagram.com/kpcapitulo" rel="noopener">Instagram &middot; @kpcapitulo</a>
            <a href="https://tiktok.com/@kp.capitulo" rel="noopener">TikTok &middot; @kp.capitulo</a>
            <a href="contact.html">Contact</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="kicker center reveal" style="justify-content:center;margin-bottom:var(--s7)">In Conversation</div>
      <div class="accordion reveal">
        <div class="acc-item"><button class="acc-trigger" type="button"><span class="q">Where did <em>The Listening Dark</em> begin?</span><span class="ico" aria-hidden="true"></span></button><div class="acc-panel"><div class="acc-panel-inner">In sixth grade, with a YA novel that convinced KP magic was real &mdash; and in 2017, when she finally started writing her own. The book has been rewritten more times than she can count, and the last words were typed during her baby&rsquo;s nap times.</div></div></div>
        <div class="acc-item"><button class="acc-trigger" type="button"><span class="q">What kind of story is it?</span><span class="ico" aria-hidden="true"></span></button><div class="acc-panel"><div class="acc-panel-inner">Adult fantasy with romance, dragons, and found family &mdash; a heroine who doesn&rsquo;t know what she is yet, a world with its own mythology, and a lore that builds gradually. Trust it.</div></div></div>
        <div class="acc-item"><button class="acc-trigger" type="button"><span class="q">Who is it for?</span><span class="ico" aria-hidden="true"></span></button><div class="acc-panel"><div class="acc-panel-inner">For those whose minds are in the stars while their feet are on the ground &mdash; surviving the real world, and loving it anyway. (Adult readers: 18+.)</div></div></div>
      </div>
    </div>
  </section>

  <section class="section-sm">
    <div class="wrap">
      <div class="kicker center reveal" style="justify-content:center;margin-bottom:var(--s5)">The Road to Publication</div>
      <div class="timeline reveal">
        <div class="tl-item"><div class="tl-date">2017</div><h3>The first draft</h3><p>A world that started in a notebook and refused to stay there.</p></div>
        <div class="tl-item"><div class="tl-date">2017 &ndash; 2024</div><h3>The rewrites</h3><p>More of them than she can count. The story kept growing; so did the writer.</p></div>
        <div class="tl-item"><div class="tl-date">2025</div><h3>Beta copies go out</h3><p>The manuscript reaches its first readers as an advance beta copy.</p></div>
        <div class="tl-item"><div class="tl-date">{PUB_DATE}</div><h3>Publication day</h3><p>The Kindle edition is <a href='{KINDLE_URL}' target='_blank' rel='noopener'>{AVAIL}</a>.</p></div>
      </div>
    </div>
  </section>

{waitlist_section()}"""

# ---------- PRESS ----------
PRESS = f"""  <header class="page-hero">
    <div class="wrap">
      <div class="kicker center reveal">Press Kit</div>
      <h1 class="reveal">For the Press</h1>
      <p class="lede reveal">Assets and press materials for <em>The Listening Dark</em> are coming soon.</p>
    </div>
  </header>

  <section class="section-sm">
    <div class="wrap" style="text-align:center">
      {DIV_STAR}
      <p class="reveal" style="font-family:var(--f-read);color:var(--ash);max-width:44ch;margin:var(--s6) auto 0">The press kit is being put together &mdash; fact sheet, cover art, author photo, and downloadable assets are on the way.</p>
      <p class="reveal" style="font-family:var(--f-read);color:var(--ash);max-width:44ch;margin:var(--s5) auto var(--s7)">For interviews, advance copies, and rights enquiries in the meantime, get in touch.</p>
      <a class="btn btn-primary reveal" href="contact.html">Contact for Press</a>
    </div>
  </section>

{waitlist_section()}"""

# ---------- FAQ ----------
def faq_item(q, a):
    return f"""<div class="acc-item"><button class="acc-trigger" type="button"><span class="q">{q}</span><span class="ico" aria-hidden="true"></span></button><div class="acc-panel"><div class="acc-panel-inner">{a}</div></div></div>"""

SIGNED_FAQ = ssi("faq-signed", faq_item("Will there be a paperback or hardcover?", "Yes &mdash; the <a href='" + PAPERBACK_URL + "' target='_blank' rel='noopener'>paperback is out now on Amazon</a>, and a hardcover is on its way. <a href='index.html#signed'>Signed copies</a> aren&rsquo;t on sale right now; <a href='#waitlist'>leave your email</a> and you&rsquo;ll hear when they are."))

FAQ = f"""  <header class="page-hero">
    <div class="wrap">
      <div class="kicker center reveal">FAQ</div>
      <h1 class="reveal">Questions in the Dark</h1>
      <p class="lede reveal">What we can tell you so far.</p>
    </div>
  </header>

  <section class="section-sm">
    <div class="wrap">
      <div class="accordion reveal">
        {faq_item("When does The Listening Dark come out?", PUB_DATE + ". The Kindle edition is <a href='" + KINDLE_URL + "' target='_blank' rel='noopener'>" + AVAIL + " on Amazon</a>.")}
        {faq_item("What is it about?", "An adult fantasy romance: a girl hidden her whole life from the academy that classifies magic, the power waking in her blood that fits no classification, and the dragons &mdash; and people &mdash; who choose her. A fuller synopsis lives on <a href='book.html'>The Book</a>.")}
        {faq_item("Is it a series?", "Yes &mdash; this is Book One. Some threads are deliberately left open; not everything is meant to close in the first book.")}
        {faq_item("Is it for me?", "It&rsquo;s adult fantasy &mdash; explicit content, violence, and language. Recommended 18+.")}
        {SIGNED_FAQ}
        {faq_item("Can I read a sample?", ("Once the Kindle edition is out, the" if PRE_ORDER else "The") + " &ldquo;Read sample&rdquo; button on its <a href='" + KINDLE_URL + "' target='_blank' rel='noopener'>Amazon page</a> gives you the opening pages free.")}
        {faq_item("How do I get an advance or review copy?", "Reviewers, press, and book folk can reach out via <a href='contact.html'>Contact</a>.")}
      </div>
    </div>
  </section>

{waitlist_section()}"""

# ---------- CONTACT ----------
CONTACT = """  <header class="page-hero">
    <div class="wrap">
      <div class="kicker center reveal">Contact</div>
      <h1 class="reveal">Say Something</h1>
      <p class="lede reveal">Press, review copies, rights, or a word for the author &mdash; the dark is listening.</p>
    </div>
  </header>

  <section class="section-sm">
    <div class="wrap">
      <form class="form reveal" data-contact novalidate>
        <div class="form-row">
          <div class="field-box"><label for="c-name">Name</label><input id="c-name" type="text" autocomplete="name"></div>
          <div class="field-box"><label for="c-email">Email</label><input id="c-email" type="email" autocomplete="email" required></div>
        </div>
        <div class="field-box"><label for="c-subject">Subject</label><input id="c-subject" type="text"></div>
        <div class="field-box"><label for="c-message">Message</label><textarea id="c-message"></textarea></div>
        <div class="hp" aria-hidden="true"><label>Leave blank<input type="text" tabindex="-1" autocomplete="off"></label></div>
        <div>
          <button class="btn btn-primary" type="submit">Send Message</button>
          <p class="form-msg" role="status" aria-live="polite" style="margin-top:var(--s5)"></p>
        </div>
      </form>
    </div>
  </section>
"""

# ---------- LEGAL ----------
def legal_body(title, lede, sections):
    secs = "".join(f"<h2>{h}</h2>{b}" for h, b in sections)
    return f"""  <header class="page-hero">
    <div class="wrap">
      <div class="kicker center reveal">Legal</div>
      <h1 class="reveal">{title}</h1>
      <p class="lede reveal">{lede}</p>
    </div>
  </header>

  <section class="section-sm">
    <div class="wrap">
      <div class="doc reveal">
        <p class="updated">Last updated &middot; {datetime.date.today():%B %Y}</p>
        {secs}
      </div>
    </div>
  </section>
"""

CONTACT_EMAIL = '<a href="mailto:author.kpcap@gmail.com">author.kpcap@gmail.com</a>'

# signed-copy wording joins the legal pages only once she switches the shop on
ORDER_LI = ("<li><strong>Signed-copy orders</strong> &mdash; your name, email address and shipping address, and any name you give for the dedication, entered at checkout. Card details go to Stripe only; we never see or store them.</li>"
            if SHOP_ENABLED else "")
ORDERS_SECTION = [("Orders",
     "<p>Signed copies are sold through <a href='https://stripe.com/privacy' rel='noopener'>Stripe</a>, which runs the checkout page and processes your payment. We use your order details only to sign, ship and support your order: to post it by USPS, to email you a receipt and tracking number, and to handle any refund. The author signs, packs and posts every copy herself, so your name and address are shared only with USPS and the military postal service that carries the parcel.</p>"
     f"<p>Stripe keeps payment records under its own policy. We keep order records {RETENTION}, and we erase names and addresses from our order records six months after an order is delivered or closed. That covers the period in which a payment can still be disputed.</p>")] if SHOP_ENABLED else []

PRIVACY = legal_body("Privacy Policy", "How we handle the little we collect.", [
    ("Who we are",
     f"<p>This website promotes <em>The Listening Dark</em>, a novel by KP Cap. It is run by the author. For anything in this policy, contact {CONTACT_EMAIL}.</p>"),
    ("What we collect",
     ("<p>We keep it minimal. There are no accounts and no advertising on this site. The personal information we handle is what you choose to send us:</p>"
      if SHOP_ENABLED else
      "<p>We keep it minimal. There are no accounts, no payments, and no advertising on this site. The only personal information we collect is what you choose to send us:</p>")
     + "<ul><li><strong>Update signups</strong> &mdash; the email address you enter in a signup form.</li>"
     "<li><strong>Contact messages</strong> &mdash; the name, email address, subject, and message you enter in the contact form.</li>"
     + ORDER_LI + "</ul>"),
    ("How we use it",
     "<p>Your signup email is used for one thing: book news &mdash; print edition and Book Two announcements for <em>The Listening Dark</em> series. Contact messages are used only to read and reply to you. We never sell, rent, or trade your information, and we don&rsquo;t send anything unrelated to the book.</p>"),
    *ORDERS_SECTION,
    ("How it&rsquo;s delivered and stored",
     f"<p>Form submissions are delivered to the author&rsquo;s inbox by <a href='https://formsubmit.co' rel='noopener'>FormSubmit</a>, a form-to-email service that processes your submission in order to deliver it. If we later move the list to a dedicated newsletter service (such as Kit or Beehiiv), your address will be stored there under that service&rsquo;s safeguards and every email will include an unsubscribe link."
     + (" Order emails, such as your tracking number, are sent through <a href='https://www.brevo.com/legal/privacypolicy/' rel='noopener'>Brevo</a>, an email delivery service." if SHOP_ENABLED else "") + "</p>"),
    ("Your choices",
     f"<p>You can leave the list at any time &mdash; reply to any email we send, or write to {CONTACT_EMAIL}, and we&rsquo;ll remove you promptly. You can also ask what information we hold about you, ask us to correct it, or ask us to delete it entirely."
     + (" For an order, we can correct your address until it ships; we can&rsquo;t delete records we&rsquo;re required to keep for tax." if SHOP_ENABLED else "") + "</p>"),
    ("Analytics &amp; cookies",
     "<p>This site sets no cookies and runs no advertising or cross-site tracking. See the <a href='cookies.html'>Cookie Policy</a> for the full picture.</p>"),
    ("Age",
     "<p><em>The Listening Dark</em> is an adult novel (18+), and this site is intended for adult readers. We do not knowingly collect information from anyone under 18; if you believe a minor has joined the list, contact us and we&rsquo;ll remove the address.</p>"),
    ("Changes",
     "<p>If this policy changes, the update will be posted on this page with a new date at the top. Significant changes will be mentioned in an update email.</p>"),
])

TERMS = legal_body("Terms of Service", "The agreement for using this site.", [
    ("Acceptance",
     "<p>By using this website you agree to these terms. If you don&rsquo;t agree, please don&rsquo;t use the site. The site exists to share information about <em>The Listening Dark</em> and to let readers find the book, "
     + ("order a limited run of signed copies, " if SHOP_ENABLED else "") + "sign up for updates, and contact the author.</p>"),
    ("Intellectual property",
     "<p>Everything on this site &mdash; the text of <em>The Listening Dark</em>, the synopsis, the cover artwork, the title, character names, and the world of the book &mdash; is &copy; KP Cap, all rights reserved. You may browse and share links freely, and quote brief passages with credit for reviews and commentary. You may not republish extracts in full, use the artwork commercially, or train AI systems on the book&rsquo;s text, without written permission.</p>"),
    ("Content note",
     "<p>The book described on this site is adult fantasy containing explicit content, violence, and language. Site content referencing the book is intended for readers 18 and over.</p>"),
    ("Acceptable use",
     "<p>Please don&rsquo;t misuse the site: no republishing site text wholesale, no submitting forms with someone else&rsquo;s email address, and no attempting to interfere with the site&rsquo;s operation.</p>"),
    *([("Signed copies",
     ssi("terms-price", "<p><strong>Price and payment.</strong> Signed copies cost $22.00 USD per copy; shipping is shown on the order page and at checkout. Payment is in full at checkout through Stripe. Your order is accepted when payment completes and you receive a receipt.</p>")
     + "<p><strong>Limited stock.</strong> The run is limited. If a copy sells twice by mistake, the later order is cancelled and refunded in full.</p>"
     + "<p><strong>Dedications.</strong> At checkout you can give a name for the author to sign your copy to. It&rsquo;s signed exactly as you type it, so please check the spelling; once signed, a dedication can&rsquo;t be changed.</p>"
     f"<p><strong>Shipping.</strong> US and APO/FPO/DPO addresses only, by USPS. Copies ship {SIGNED_SHIPS} of payment, from a US military post office overseas, so delivery usually takes one to three weeks more. You&rsquo;ll get the tracking number by email. If we can&rsquo;t ship on time, we&rsquo;ll email you a new date and the option to cancel for a full refund. Please check your address at checkout; a parcel returned for a wrong address can be re-sent once you cover the new postage.</p>"
     + ssi("terms-refund", "<p><strong>Cancellations, returns and refunds.</strong> The refund policy for your order is the one shown at checkout and in your receipt. A copy that arrives damaged, or is lost in the mail, is always replaced or refunded.</p>"))] if SHOP_ENABLED else []),
    ("Third-party links",
     "<p>The site links to third-party platforms (Amazon, Instagram, TikTok)"
     + (", uses Stripe for checkout and USPS for delivery," if SHOP_ENABLED else "")
     + " and uses a third-party service to deliver form submissions. Those services have their own terms and policies, which we don&rsquo;t control.</p>"),
    ("No warranties",
     "<p>The site is provided as-is. Release dates, formats, and other book details are subject to change &mdash; publishing is like that. We do our best to keep everything accurate, but we can&rsquo;t guarantee it.</p>"),
    ("Liability",
     ("<p>To the fullest extent permitted by law, the author is not liable for any indirect or consequential loss arising from your use of this site. Nothing in these terms limits rights you have as a consumer under the law where you live.</p>"
      if SHOP_ENABLED else
      "<p>To the fullest extent permitted by law, the author is not liable for any indirect or consequential loss arising from your use of this informational site.</p>")),
    ("Changes",
     f"<p>These terms may be updated from time to time; the date at the top reflects the latest version. Questions: {CONTACT_EMAIL}.</p>"),
])

COOKIES = legal_body("Cookie Policy", "The crumbs we do and don&rsquo;t leave.", [
    ("The short version",
     "<p><strong>This site sets no cookies.</strong> No advertising cookies, no analytics cookies, no tracking pixels, no third-party embeds that follow you around the internet.</p>"),
    ("What actually happens",
     "<p>The site is plain HTML, CSS, and JavaScript served as static files. Nothing is stored on your device beyond your browser&rsquo;s ordinary page cache. When you submit a form, your data is sent once, to deliver your message &mdash; nothing is left behind in your browser.</p>"),
    *([("Checkout",
     "<p>When you order a signed copy, you leave this site for Stripe&rsquo;s checkout page. Stripe sets its own cookies there, on its own domain, to process the payment and prevent fraud. They&rsquo;re covered by <a href='https://stripe.com/cookie-settings' rel='noopener'>Stripe&rsquo;s cookie policy</a>, not this one.</p>")] if SHOP_ENABLED else []),
    ("If that ever changes",
     "<p>If we ever add analytics, it will be a privacy-first, cookieless tool, and this page will be updated first with a new date at the top.</p>"),
    ("Managing cookies",
     f"<p>Because we don&rsquo;t set any, there&rsquo;s nothing to manage here &mdash; but you can always control cookies globally in your browser&rsquo;s privacy settings. Questions: {CONTACT_EMAIL}.</p>"),
])
ACCESS = legal_body("Accessibility Statement", "Everyone should get to enter the dark.", [
    ("Our commitment", "<p>We aim to meet WCAG 2.2 AA. The site supports keyboard navigation, honours reduced-motion preferences, and maintains comfortable colour contrast on every text element.</p>"),
    ("Measures we take", "<ul><li>Keyboard-navigable with visible focus states</li><li>Respects <em>prefers-reduced-motion</em></li><li>No flashing, flickering, or animated background textures</li><li>Semantic structure and descriptive links</li><li>All text meets or exceeds AA contrast</li></ul>"),
    ("Feedback", "<p>Found a barrier? Please tell us via the <a href='contact.html'>contact page</a> and we&rsquo;ll put it right.</p>"),
])

# ---------- 404 ----------
NOTFOUND = """  <section class="err">
    <div class="code">Error 404</div>
    <h1>The dark didn&rsquo;t hear that.</h1>
    <p>The page you&rsquo;re listening for isn&rsquo;t here &mdash; or isn&rsquo;t here yet.</p>
    <a class="btn btn-primary" href="index.html">Back to the beginning</a>
  </section>
"""

# ---------- THANK YOU (stripe success_url) ----------
# anyone can open this url, so it never claims the payment went through; the stripe receipt does
THANKS = f"""  <header class="page-hero">
    <div class="wrap">
      <div class="kicker center reveal">Signed copies</div>
      <h1 class="reveal">Thank you.</h1>
      <p class="lede reveal">If you&rsquo;ve just ordered a signed copy, your receipt from Stripe is on its way. That receipt is your confirmation.</p>
    </div>
  </header>

  <section class="section-sm">
    <div class="wrap">
      <div class="doc reveal">
        <h2>What happens next</h2>
        <ol>
          <li>KP Capitulo signs and packs your copy.</li>
          <li>It ships by USPS {SIGNED_SHIPS}, from a US military post office overseas, so allow one to three weeks more for delivery.</li>
          <li>You get a second email with the tracking number the day it goes out.</li>
        </ol>
        <p>If you added a name for the dedication, KP Capitulo signs your copy to it, exactly as you typed it.</p>
        <h2>Wrong address?</h2>
        <p>Write to {CONTACT_EMAIL} as soon as you can, with the name you used at checkout. We can fix it any time before your copy ships.</p>
        <h2>No receipt?</h2>
        <p>Give it a few minutes, then check your spam or promotions folder. Still nothing after an hour? Write to {CONTACT_EMAIL} with the name and email you used at checkout. Please don&rsquo;t order again to check; it would charge you twice.</p>
        <p>Left checkout before paying? Then nothing was charged.</p>
        <p><a class="link-txt" href="index.html">Back to the beginning <span class="arrow" aria-hidden="true">&rarr;</span></a></p>
      </div>
    </div>
  </section>
"""

NOINDEX = """<meta name="robots" content="noindex">
"""

# ---------- CHECKOUT UNAVAILABLE (nginx sends failed or rate-limited checkouts here) ----------
UNAVAILABLE = f"""  <header class="page-hero">
    <div class="wrap">
      <div class="kicker center reveal">Signed copies</div>
      <h1 class="reveal">Checkout is resting.</h1>
      <p class="lede reveal">Nothing was charged. The signed copies may have just sold out, or fewer are left than you chose. Check the <a href="index.html#signed">signed copy section</a> for what&rsquo;s available now, or try again in a few minutes.</p>
    </div>
  </header>

  <section class="section-sm">
    <div class="wrap">
      <div class="doc reveal">
        <p>If it keeps happening, write to {CONTACT_EMAIL} and we&rsquo;ll sort it out.</p>
        <p><a class="link-txt" href="index.html#signed">Back to the signed copy <span class="arrow" aria-hidden="true">&rarr;</span></a></p>
      </div>
    </div>
  </section>
"""

# =====================================================================
#  BUILD
# =====================================================================
import json
EBOOK_OFFER = {"@type": "Offer", "url": KINDLE_URL,
               "availability": "https://schema.org/" + ("PreOrder" if PRE_ORDER else "InStock")}
BOOK_DATA = {
    "@context": "https://schema.org",
    "@type": "Book",
    "name": "The Listening Dark",
    "author": {"@type": "Person", "name": "KP Capitulo"},
    "genre": "Adult Fantasy Romance",
    "bookFormat": "https://schema.org/EBook",
    "datePublished": PUB_DATE_ISO,
    "image": SITE + "/assets/cover.jpg",
    "url": SITE + "/book.html",
    "offers": EBOOK_OFFER,
}
# json.dumps leaves "<" alone, so a stray "</script>" in any value would end the block
# the signed edition rides on the same line with an empty stub, so the fallback page is today's page
BOOK_LD = ('<script type="application/ld+json">' + json.dumps(BOOK_DATA).replace("<", "\\u003c") + "</script>"
           + (ssi("ld-signed", "") if SHOP_ENABLED else "") + "\n")
page("index.html", "The Listening Dark — an adult fantasy romance by KP Cap",
     "Dragons choose their riders. Something older chose her. The Listening Dark, Book One of KP Cap's adult romantasy debut. Out on Kindle October 30, 2026.",
     "home", HOME, wl_target="#waitlist", extra_head=BOOK_LD)
page("book.html", "The Book — The Listening Dark",
     "The Listening Dark, Book One: an adult fantasy romance about a power that refuses classification, the academy that hunts it, and the dragon that has been waiting.",
     "book", BOOK, wl_target="#waitlist", extra_head=BOOK_LD)
page("author.html", "The Author — KP Cap",
     "KP Cap — military spouse, world-builder since sixth grade, debut romantasy author. The Listening Dark was written between 2017 and her baby's nap times.",
     "author", AUTHOR, wl_target="#waitlist")
page("press.html", "Press Kit — The Listening Dark",
     "Press materials for The Listening Dark by KP Cap are coming soon. Interview and review enquiries welcome.",
     "press", PRESS, wl_target="#waitlist")
page("faq.html", "FAQ — The Listening Dark",
     "Frequently asked questions about The Listening Dark by KP Cap — release, series plans, content notes, and samples.",
     "faq", FAQ, wl_target="#waitlist")
page("contact.html", "Contact — The Listening Dark",
     "Contact KP Cap for press, advance copies, rights, and events regarding The Listening Dark.",
     "contact", CONTACT, wl_target="index.html#waitlist")
page("privacy.html", "Privacy Policy — The Listening Dark",
     "Privacy policy for The Listening Dark.", "", PRIVACY, wl_target="index.html#waitlist")
page("terms.html", "Terms of Service — The Listening Dark",
     "Terms of service for The Listening Dark.", "", TERMS, wl_target="index.html#waitlist")
page("cookies.html", "Cookie Policy — The Listening Dark",
     "Cookie policy for The Listening Dark.", "", COOKIES, wl_target="index.html#waitlist")
page("accessibility.html", "Accessibility Statement — The Listening Dark",
     "Accessibility statement for The Listening Dark.", "", ACCESS, wl_target="index.html#waitlist")
SHOP_PAGES = {"thank-you.html": ("Thank you — The Listening Dark", "After checkout for a signed copy of The Listening Dark.", THANKS),
              "checkout-unavailable.html": ("Checkout unavailable — The Listening Dark", "Checkout for signed copies is briefly unavailable.", UNAVAILABLE)}
for fn, (title, desc, body) in SHOP_PAGES.items():
    if SHOP_ENABLED:
        page(fn, title, desc, "", body, wl_target="index.html#waitlist", extra_head=NOINDEX, listed=False)
# a page left by an earlier build must go, and the disclosure page is gone for good (D8)
for stale in ([] if SHOP_ENABLED else list(SHOP_PAGES)) + ["commerce-disclosure.html"]:
    if os.path.exists(os.path.join(ROOT, stale)):
        os.remove(os.path.join(ROOT, stale))
        print("removed", stale, "- commit the deletion, or the deploy pull leaves it live")
page("404.html", "Not Found — The Listening Dark",
     "The page you are listening for isn't here.", "", NOTFOUND, wl_target="index.html#waitlist", listed=False)

with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{u}</loc></url>\n" for u in PAGES) + "</urlset>\n")
print("wrote robots.txt, sitemap.xml")

print("\nDone. Built into:", ROOT)
