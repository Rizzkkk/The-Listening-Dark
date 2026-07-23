#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site generator for THE LISTENING DARK by KP Cap.
An adult fantasy romance (romantasy) — Book One of a new series.

Emits plain HTML files into the project root from shared fragments,
so the nav/footer stay identical across every page.
Run:  python tools/build.py
Output is standard HTML/CSS/JS — no runtime dependency on this script.

Excerpts, quotes and author bio are taken from the author's own
manuscript / beta copy with permission (this is the author's site).
"""
import os, base64, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YEAR = datetime.date.today().year

# ---- Favicon: twin moons on the night ground ----
FAVICON_SVG = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='#141119'/><circle cx='13' cy='14' r='8' stroke='#A78FE3' stroke-width='1.4' fill='none' opacity='.9'/><circle cx='21' cy='20' r='4.5' fill='#D2A85E' opacity='.95'/><circle cx='24.5' cy='7.5' r='1.1' fill='#E6E3F2'/></svg>"""
FAVICON = "data:image/svg+xml;base64," + base64.b64encode(FAVICON_SVG.encode()).decode()

# ---- The twin-moon mark (Twin Moon Rite) — nav / footer ----
MARK = """<svg class="mark" viewBox="0 0 32 32" fill="none" aria-hidden="true"><circle cx="13" cy="14" r="8.5" stroke="#A78FE3" stroke-width="1.3" opacity=".9"/><circle cx="21.5" cy="20" r="5" fill="#D2A85E" opacity=".95"/><circle cx="25" cy="7.5" r="1.1" fill="#E6E3F2"/></svg>"""

# small mark for cover / empty states
MOON_SM = """<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" width="40" height="40"><circle cx="13" cy="14" r="8.5" stroke="#A78FE3" stroke-width="1.2" opacity=".9"/><circle cx="21.5" cy="20" r="5" fill="#D2A85E" opacity=".95"/><circle cx="25" cy="7.5" r="1.1" fill="#E6E3F2"/></svg>"""

DIV_STAR = """<div class="divider-star" aria-hidden="true"><span>&#10022;&nbsp;&nbsp;&#10022;</span></div>"""

def head(title, desc):
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
<meta property="og:image" content="assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="assets/og.png">
<link rel="icon" href="{FAVICON}">
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/fraunces.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/inter.woff2" crossorigin>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="sky" aria-hidden="true"></div>
"""

def nav(active, wl_target):
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
      {links}
      <a class="btn btn-primary btn-mini" href="{wl_target}">Join the Waitlist</a>
    </div>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  </div>
</nav>
<div class="menu" id="menu" aria-hidden="true">
  <nav class="menu-links" aria-label="Mobile">
    <a href="index.html">Home</a>
    <a href="book.html">The Book</a>
    <a href="author.html">The Author</a>
    <a href="press.html">Press</a>
    <a href="faq.html">FAQ</a>
  </nav>
  <div class="menu-foot">
    <a class="btn btn-primary" href="{wl_target}">Join the Waitlist</a>
    <div class="menu-social"><a href="https://instagram.com/kpcapitulo" rel="noopener">Instagram</a><a href="https://tiktok.com/@kp.capitulo" rel="noopener">TikTok</a><a href="contact.html">Contact</a></div>
  </div>
</div>
"""

# ---- The real cover art (cropped from the author's hardcover design) ----
def cover_block(large=False):
    cls = "cover cover-img lg" if large else "cover cover-img"
    return f"""<div class="cover-stage reveal">
          <div class="{cls}" id="cover">
            <img src="assets/cover.jpg" alt="The Listening Dark by KP Cap &mdash; front cover: a woman in a dark gown beneath twin moons, before a candlelit gothic castle, framed in silver filigree" width="900" height="1564" loading="lazy">
          </div>
        </div>"""

def waitlist_section():
    return """  <section class="section waitlist" id="waitlist">
    <div class="wrap">
      <div class="card-wl reveal">
        <div class="kicker center" style="margin-bottom:var(--s5)">The Invitation</div>
        <h2>Be the first<br>into the dark.</h2>
        <p class="lead">Join the waitlist for the cover reveal, early chapters, and word of when <em>The Listening Dark</em> arrives.</p>
        <form class="wl-form" data-waitlist novalidate>
          <div class="hp" aria-hidden="true"><label>Leave blank<input type="text" tabindex="-1" autocomplete="off"></label></div>
          <div class="field"><input type="email" placeholder="Enter your email" aria-label="Email address" required></div>
          <button class="btn btn-primary" type="submit">Join the Waitlist</button>
        </form>
        <p class="form-msg" role="status" aria-live="polite"></p>
        <p class="wl-note">No noise. One message when it matters. Unsubscribe anytime.</p>
      </div>
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
          <a href="book.html">The Book</a><a href="book.html#excerpt">Chapter One</a><a href="author.html">The Author</a><a href="press.html">Press Kit</a>
        </div>
        <div class="foot-col">
          <h4>Connect</h4>
          <a href="{wl_target}">Join the Waitlist</a><a href="contact.html">Contact</a><a href="https://instagram.com/kpcapitulo" rel="noopener">Instagram</a><a href="https://tiktok.com/@kp.capitulo" rel="noopener">TikTok</a>
        </div>
        <div class="foot-col foot-mini">
          <h4>Enter the dark first</h4>
          <p>The cover reveal and early chapters, straight to you.</p>
          <form data-waitlist novalidate>
            <div class="hp" aria-hidden="true"><label>Leave blank<input type="text" tabindex="-1" autocomplete="off"></label></div>
            <div class="field"><input type="email" placeholder="you@email.com" aria-label="Email address" required><button class="btn btn-primary btn-mini" type="submit">Join</button></div>
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

def page(filename, title, desc, active, body, wl_target="#waitlist"):
    html = head(title, desc) + nav(active, wl_target) + '<main class="content" id="main"><span id="top"></span>\n' + body + footer(wl_target)
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename, f"({len(html)} bytes)")

# =====================================================================
#  REAL CONTENT — from the manuscript
# =====================================================================

# Chapter One, opening (verbatim from the beta manuscript)
EXCERPT_OPEN = """<p class="dropcap">&ldquo;I can&rsquo;t think of anything I want more than to stop running,&rdquo; I grumbled as we jogged through the chilly morning air.</p>
<p>The rustle of trees, birdsong overhead, the steady rhythm of my breath &mdash; it all usually calmed me. Today, my chest felt too tight for comfort.</p>
<p>&ldquo;Please,&rdquo; Dezi laughed. &ldquo;You say that every time. Just focus on breakfast. You&rsquo;ll survive.&rdquo;</p>
<p>&ldquo;You say that every time too,&rdquo; I shot back.</p>
<p>She grinned without looking at me, the way she always did when she knew she was right and didn&rsquo;t need to prove it. That was Dezi. She&rsquo;d been winning arguments with silence for as long as either of us could remember.</p>
<p>A few paces ahead, she lifted two fingers and flicked them idly toward a cluster of fallen leaves on the path. They skittered aside without the wind touching them, clearing a neat little corridor for her feet. She didn&rsquo;t even look down. Just kept running.</p>
<p>I rolled my eyes. &ldquo;You&rsquo;re going to trip over yourself showing off to no one.&rdquo;</p>
<p>&ldquo;I&rsquo;m not showing off,&rdquo; she said pleasantly. &ldquo;I&rsquo;m optimizing.&rdquo;</p>"""

EXCERPT_MORE = """<p>Neither of us had what you&rsquo;d call <em>real</em> magic. Nobody in town did. What we had was smaller than that &mdash; minor things, quiet things. The kind of magic you didn&rsquo;t talk about in front of parents or strangers. Dezi could nudge objects, coax small flames, make the air around her go still or restless depending on her mood. I was less comfortable with mine. I could feel things before they happened sometimes &mdash; a pressure behind my sternum, a knowing that arrived half a second too early. I didn&rsquo;t like it. It felt less like a gift and more like something trying to get my attention.</p>
<p>I ignored it when I could.</p>
<p>This morning it felt like it was pressing too close.</p>
<p>We rounded the bend where the path split &mdash; left toward the caf&eacute;, right toward the tree line that marked the edge of town. The invisible boundary our parents had drawn for us before we were old enough to push back against it.</p>
<p>Dezi&rsquo;s steps slowed.</p>
<p>I already knew what she was going to say before she said it.</p>
<p>&ldquo;We could just look,&rdquo; she said, tilting her head toward the trees on the right. &ldquo;We don&rsquo;t have to go past the line. Just look.&rdquo;</p>
<p>&ldquo;We are not doing this again.&rdquo;</p>
<p>&ldquo;The border is imaginary, Cam.&rdquo;</p>
<p>&ldquo;The border is our parents&rsquo; entire personality,&rdquo; I said. &ldquo;And I would like to keep mine intact, thank you.&rdquo;</p>
<p>&ldquo;My mother used to say magic is just the world paying attention to you,&rdquo; Dezi said. &ldquo;That some people the world notices more than others.&rdquo;</p>"""

# =====================================================================
#  PAGE BODIES
# =====================================================================

HOME = f"""  <header class="hero">
    <div class="hero-moons" aria-hidden="true"></div>
    <div class="hero-inner">
      <div class="kicker center eyebrow" data-reveal>An Adult Fantasy Romance &middot; Book One &middot; KP&nbsp;Cap</div>
      <h1 class="hero-title" data-split>The Listening Dark</h1>
      <p class="hero-sub" data-reveal>It doesn&rsquo;t respond to will. It doesn&rsquo;t obey. <b>It listens.</b></p>
      <div class="hero-cta" data-reveal>
        <a class="btn btn-primary" href="#waitlist">Join the Waitlist</a>
        <a class="btn btn-ghost" href="#excerpt">Read Chapter One</a>
      </div>
    </div>
    <div class="scrollcue" aria-hidden="true"><span>Scroll</span><span class="bar"></span></div>
  </header>

  <section class="section logline">
    <div class="wrap">
      <div class="kicker center reveal">The Premise</div>
      <p class="reveal">Some doors aren&rsquo;t locked. <span class="accent">They&rsquo;re simply not for everyone.</span></p>
    </div>
  </section>

  <section class="section" id="book">
    <div class="wrap">
      <div class="book-grid">
        {cover_block(False)}
        <div class="prose-head">
          <div class="kicker reveal">The Story</div>
          <h2 class="reveal">Dragons choose their riders. Something older chose her.</h2>
          <div class="prose reveal">
            <p>When Camilla Ayala is dragged to Etereia &mdash; the realm where those born with extraordinary abilities are trained, classified, and controlled &mdash; she arrives with nothing but grief and a power no one can name. It doesn&rsquo;t respond to will. It doesn&rsquo;t obey. <em>It listens.</em></p>
            <p>Then there&rsquo;s the dragon. Ancient beyond measure. Calling to her in the dark.</p>
          </div>
          <dl class="spec reveal">
            <div><dt>Genre</dt><dd>Adult Fantasy Romance</dd></div>
            <div><dt>Series</dt><dd>Book One</dd></div>
            <div><dt>Publication</dt><dd>To Be Announced</dd></div>
          </dl>
          <a class="link-txt reveal" href="book.html">More about the book <span class="arrow">&rarr;</span></a>
        </div>
      </div>
    </div>
  </section>

  <section class="section quote">
    <div class="wrap">
      {DIV_STAR}
      <blockquote class="reveal">&ldquo;Magic is just the world <em>paying attention</em> to you. Some people the world notices more than others.&rdquo;</blockquote>
      <cite class="reveal">From Chapter One</cite>
    </div>
  </section>

  <section class="section" id="excerpt">
    <div class="wrap">
      <div class="reading">
        <div class="kicker center reveal">Chapter One</div>
        <div class="gate locked" id="home-gate">
          <div class="reading-body reveal">
            {EXCERPT_OPEN}
          </div>
        </div>
        <div class="gate-cta reveal">
          <div class="kicker center">Keep reading</div>
          <a class="btn btn-primary" href="book.html#excerpt">Continue Chapter One</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section-sm">
    <div class="wrap" style="text-align:center">
      <div class="kicker center reveal" style="justify-content:center;margin-bottom:var(--s5)">The Author</div>
      <p class="reveal" style="font-family:var(--f-display);font-variation-settings:'opsz' 96,'wght' 380;font-size:clamp(1.6rem,3.6vw,2.6rem);letter-spacing:-.01em;margin:0 auto var(--s5);max-width:26ch;color:var(--bone-bright)">KP Cap has been building this world since 2017 &mdash; and finished it during her baby&rsquo;s nap times.</p>
      <a class="link-txt reveal" href="author.html" style="justify-content:center">Meet the author <span class="arrow">&rarr;</span></a>
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
          <h2 class="reveal">What the dark hears, it keeps.</h2>
          <div class="prose reveal">
            <p>When Camilla Ayala is dragged to Etereia, the realm where those born with extraordinary abilities are trained, classified, and controlled, she arrives with nothing but grief and a power no one can name. Etereia classifies everything. Every gift, every ability, every threat. But the cold, quiet force beneath Camilla&rsquo;s skin won&rsquo;t cooperate with their systems. It doesn&rsquo;t respond to will. It doesn&rsquo;t obey. <em>It listens.</em> And the people who run this place have very specific plans for things they can&rsquo;t categorize.</p>
            <p>Then there&rsquo;s the dragon. Ancient beyond measure. Calling to her in the dark.</p>
            <p>And the rider who trains her without being asked, who sees through every wall she builds, who looks at her like he&rsquo;s waiting for her to remember something she&rsquo;s never known.</p>
            <p>Camilla didn&rsquo;t come to Etereia to change anything. But some powers don&rsquo;t ask permission. And some truths, once they start surfacing, don&rsquo;t know how to stop.</p>
            <p><em>The Listening Dark</em> is an adult fantasy novel about power that can&rsquo;t be contained, origins that were never meant to be found, and what happens when the world you were hidden from decides it wants you back.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section quote">
    <div class="wrap">
      {DIV_STAR}
      <blockquote class="reveal">&ldquo;Magic is not merely a force &mdash; it is a relationship. Between the self and the world. Between what exists and <em>what it reaches toward.</em>&rdquo;</blockquote>
      <cite class="reveal">From <em>The Listening Dark</em></cite>
    </div>
  </section>

  <section class="section" id="excerpt">
    <div class="wrap">
      <div class="reading">
        <div class="kicker center reveal">Read the Opening &middot; Chapter One</div>
        <div class="gate locked" id="book-gate">
          <div class="reading-body reveal">
            {EXCERPT_OPEN}
            {EXCERPT_MORE}
          </div>
        </div>
        <div class="gate-cta reveal">
          <div class="kicker center">Keep reading</div>
          <a class="btn btn-primary" href="#waitlist">Join the waitlist to read on</a>
          <div style="margin-top:var(--s4)"><button class="link-txt" type="button" data-unlock="#book-gate">Or finish this excerpt <span class="arrow">&darr;</span></button></div>
        </div>
      </div>
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
        <div><dt>Formats</dt><dd>To Be Announced</dd></div>
        <div><dt>Publication</dt><dd>To Be Announced</dd></div>
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
      <h1 class="reveal">KP Cap</h1>
      <p class="lede reveal">Dreaming up fantasy worlds since the sixth grade. Writing this one since 2017.</p>
    </div>
  </header>

  <section class="section-sm">
    <div class="wrap">
      <div class="author-grid">
        <figure class="portrait reveal" style="margin:0">
          <!-- AUTHOR PHOTO PLACEHOLDER
               When the photo is ready, drop it at assets/author.jpg and
               uncomment the line below (then delete the placeholder marks):
          <img src="assets/author.jpg" alt="KP Cap, author of The Listening Dark">
          -->
          <span class="pmark">{MOON_SM}</span>
          <figcaption class="p-note">Author photo &mdash; coming soon</figcaption>
        </figure>
        <div class="author-bio">
          <div class="kicker reveal">Biography</div>
          <div class="prose reveal" style="margin-top:var(--s5)">
            <p><strong>KP Cap</strong> is a military spouse, a collector of random trinkets, and the kind of person who started writing a fantasy novel in 2017, rewrote it more times than she can count, and finally finished it during her baby&rsquo;s nap times &mdash; which, if you know newborns, makes this book an act of sheer determination.</p>
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
        <div class="tl-item"><div class="tl-date">Coming soon</div><h3>Publication day</h3><p>Date to be announced. The waitlist hears it first.</p></div>
      </div>
    </div>
  </section>

{waitlist_section()}"""

# ---------- PRESS ----------
def asset(name, meta, icon, href="#", live=False):
    dl = ' download' if live else ''
    return f"""<div class="asset"><div class="thumb">{icon}</div><div><div class="a-name">{name}</div><div class="a-meta">{meta}</div></div><a class="btn btn-ghost btn-mini" href="{href}"{dl} aria-label="Download {name}">Download</a></div>"""

ICON_IMG = """<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="1.3"/><circle cx="8.5" cy="10" r="1.5" fill="currentColor"/><path d="M4 17l5-4 4 3 3-2 4 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
ICON_DOC = """<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 3h8l4 4v14H6z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/><path d="M14 3v4h4M9 12h6M9 15h6M9 9h2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>"""

PRESS = f"""  <header class="page-hero">
    <div class="wrap">
      <div class="kicker center reveal">Press Kit</div>
      <h1 class="reveal">For the Press</h1>
      <p class="lede reveal">Everything you need to write about <em>The Listening Dark</em> and KP&nbsp;Cap.</p>
    </div>
  </header>

  <section class="section-sm">
    <div class="wrap">
      <div class="kicker reveal" style="margin-bottom:var(--s7)">Downloads</div>
      <div class="grid grid-3 stagger">
        {asset("Book cover (web res)", "JPG &middot; 900&times;1564 &middot; available now", ICON_IMG, "assets/cover.jpg", True)}
        {asset("Author photo", "JPG &middot; coming soon", ICON_IMG)}
        {asset("Title logo &amp; twin-moon mark", "SVG &middot; PNG &middot; coming soon", ICON_DOC)}
        {asset("One-sheet", "PDF &middot; coming soon", ICON_DOC)}
        {asset("Sample chapter", "PDF &middot; coming soon", ICON_DOC)}
        {asset("Full press kit", "ZIP &middot; coming soon", ICON_DOC)}
      </div>
      <p class="placeholder-note reveal" style="margin-top:var(--s6)">Download links will be connected as final assets are approved.</p>
    </div>
  </section>

  <section class="section-sm">
    <div class="wrap wrap-narrow">
      <div class="kicker reveal" style="margin-bottom:var(--s6)">Fact Sheet</div>
      <dl class="spec reveal" style="border-top:1px solid var(--line)">
        <div><dt>Title</dt><dd>The Listening Dark</dd></div>
        <div><dt>Author</dt><dd>KP Cap</dd></div>
        <div><dt>Genre</dt><dd>Adult Fantasy Romance</dd></div>
        <div><dt>Series</dt><dd>Book One</dd></div>
        <div><dt>Publication</dt><dd>To Be Announced</dd></div>
        <div><dt>Audience</dt><dd>Adult &middot; 18+</dd></div>
        <div><dt>Instagram</dt><dd>@kpcapitulo</dd></div>
        <div><dt>TikTok</dt><dd>@kp.capitulo</dd></div>
      </dl>
      <div class="kicker reveal" style="margin:var(--s8) 0 var(--s5)">Boilerplate</div>
      <div class="prose reveal"><p><em>The Listening Dark</em> is the debut adult romantasy from KP Cap &mdash; a story of dragons that choose disruption, an academy that classifies every power in the realm, and a girl whose magic refuses classification. Romance, found family, and a world entirely its own. Book One of a planned series.</p></div>
    </div>
  </section>

  <section class="section-sm">
    <div class="wrap" style="text-align:center">
      <div class="kicker center reveal" style="justify-content:center;margin-bottom:var(--s5)">Press &amp; Review Enquiries</div>
      <p class="reveal" style="font-family:var(--f-read);color:var(--ash);max-width:40ch;margin:0 auto var(--s6)">For interviews, advance copies, and rights enquiries, get in touch.</p>
      <a class="btn btn-primary reveal" href="contact.html">Contact for Press</a>
    </div>
  </section>

{waitlist_section()}"""

# ---------- FAQ ----------
def faq_item(q, a):
    return f"""<div class="acc-item"><button class="acc-trigger" type="button"><span class="q">{q}</span><span class="ico" aria-hidden="true"></span></button><div class="acc-panel"><div class="acc-panel-inner">{a}</div></div></div>"""

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
        {faq_item("When does The Listening Dark come out?", "A publication date hasn&rsquo;t been announced yet &mdash; advance beta copies are with early readers now. Join the waitlist and you&rsquo;ll be the first to know.")}
        {faq_item("What is it about?", "An adult fantasy romance: a girl hidden her whole life from the academy that classifies magic, the power waking in her blood that fits no classification, and the dragons &mdash; and people &mdash; who choose her. A fuller synopsis lives on <a href='book.html'>The Book</a>.")}
        {faq_item("Is it a series?", "Yes &mdash; this is Book One. Some threads are deliberately left open; not everything is meant to close in the first book.")}
        {faq_item("Is it for me?", "It&rsquo;s adult fantasy &mdash; explicit content, violence, and language. Recommended 18+. If ACOTAR energy and Throne of Glass pacing are your thing, you&rsquo;re in the right place.")}
        {faq_item("Can I read a sample?", "The opening of Chapter One is on <a href='book.html#excerpt'>the book page</a>, with more coming to waitlist members.")}
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
      <p class="reveal" style="text-align:center;margin-top:var(--s7);font-family:var(--f-read);color:var(--ash)">Prefer email? Write directly to <a href="mailto:author.kpcap@gmail.com" style="color:var(--ember);text-decoration:underline;text-underline-offset:3px">author.kpcap@gmail.com</a></p>
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

PRIVACY = legal_body("Privacy Policy", "How we handle the little we collect.", [
    ("Who we are",
     f"<p>This website promotes <em>The Listening Dark</em>, a novel by KP Cap. It is run by the author. For anything in this policy, contact {CONTACT_EMAIL}.</p>"),
    ("What we collect",
     "<p>We keep it minimal. There are no accounts, no payments, and no advertising on this site. The only personal information we collect is what you choose to send us:</p>"
     "<ul><li><strong>Waitlist signups</strong> &mdash; the email address you enter in a waitlist form.</li>"
     "<li><strong>Contact messages</strong> &mdash; the name, email address, subject, and message you enter in the contact form.</li></ul>"),
    ("How we use it",
     "<p>Your waitlist email is used for one thing: book news &mdash; the cover reveal, early chapters, and release announcements for <em>The Listening Dark</em>. Contact messages are used only to read and reply to you. We never sell, rent, or trade your information, and we don&rsquo;t send anything unrelated to the book.</p>"),
    ("How it&rsquo;s delivered and stored",
     f"<p>Form submissions are delivered to the author&rsquo;s inbox by <a href='https://formsubmit.co' rel='noopener'>FormSubmit</a>, a form-to-email service that processes your submission in order to deliver it. If we later move the list to a dedicated newsletter service (such as Kit or Beehiiv), your address will be stored there under that service&rsquo;s safeguards and every email will include an unsubscribe link.</p>"),
    ("Your choices",
     f"<p>You can leave the list at any time &mdash; reply to any email we send, or write to {CONTACT_EMAIL}, and we&rsquo;ll remove you promptly. You can also ask what information we hold about you, ask us to correct it, or ask us to delete it entirely.</p>"),
    ("Analytics &amp; cookies",
     "<p>This site sets no cookies and runs no advertising or cross-site tracking. See the <a href='cookies.html'>Cookie Policy</a> for the full picture.</p>"),
    ("Age",
     "<p><em>The Listening Dark</em> is an adult novel (18+), and this site is intended for adult readers. We do not knowingly collect information from anyone under 18; if you believe a minor has joined the list, contact us and we&rsquo;ll remove the address.</p>"),
    ("Changes",
     "<p>If this policy changes, the update will be posted on this page with a new date at the top. Significant changes will be mentioned in a waitlist email.</p>"),
])

TERMS = legal_body("Terms of Service", "The agreement for using this site.", [
    ("Acceptance",
     "<p>By using this website you agree to these terms. If you don&rsquo;t agree, please don&rsquo;t use the site. The site exists to share information about <em>The Listening Dark</em> and to let readers join the waitlist and contact the author.</p>"),
    ("Intellectual property",
     "<p>Everything on this site &mdash; the text of <em>The Listening Dark</em>, including the Chapter One excerpt, the synopsis, the cover artwork, the title, character names, and the world of the book &mdash; is &copy; KP Cap, all rights reserved. You may browse and share links freely, and quote brief passages with credit for reviews and commentary. You may not republish the excerpt in full, use the artwork commercially, or train AI systems on the book&rsquo;s text, without written permission.</p>"),
    ("Content note",
     "<p>The book described on this site is adult fantasy containing explicit content, violence, and language. Site content referencing the book is intended for readers 18 and over.</p>"),
    ("Acceptable use",
     "<p>Please don&rsquo;t misuse the site: no scraping the excerpt for republication, no submitting forms with someone else&rsquo;s email address, and no attempting to interfere with the site&rsquo;s operation.</p>"),
    ("Third-party links",
     "<p>The site links to third-party platforms (Instagram, TikTok) and uses a third-party service to deliver form submissions. Those services have their own terms and policies, which we don&rsquo;t control.</p>"),
    ("No warranties",
     "<p>The site is provided as-is. Release dates, formats, and other book details are subject to change &mdash; publishing is like that. We do our best to keep everything accurate, but we can&rsquo;t guarantee it.</p>"),
    ("Liability",
     "<p>To the fullest extent permitted by law, the author is not liable for any indirect or consequential loss arising from your use of this informational site.</p>"),
    ("Changes",
     f"<p>These terms may be updated from time to time; the date at the top reflects the latest version. Questions: {CONTACT_EMAIL}.</p>"),
])

COOKIES = legal_body("Cookie Policy", "The crumbs we do and don&rsquo;t leave.", [
    ("The short version",
     "<p><strong>This site sets no cookies.</strong> No advertising cookies, no analytics cookies, no tracking pixels, no third-party embeds that follow you around the internet.</p>"),
    ("What actually happens",
     "<p>The site is plain HTML, CSS, and JavaScript served as static files. Nothing is stored on your device beyond your browser&rsquo;s ordinary page cache. When you submit a form, your data is sent once, to deliver your message &mdash; nothing is left behind in your browser.</p>"),
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

# =====================================================================
#  BUILD
# =====================================================================
page("index.html", "The Listening Dark — an adult fantasy romance by KP Cap",
     "Dragons choose their riders. Something older chose her. The Listening Dark, Book One of KP Cap's adult romantasy debut. Read Chapter One and join the waitlist.",
     "home", HOME, wl_target="#waitlist")
page("book.html", "The Book — The Listening Dark",
     "The Listening Dark, Book One: an adult fantasy romance about a power that refuses classification, the academy that hunts it, and the dragon that has been waiting. Read the opening of Chapter One.",
     "book", BOOK, wl_target="#waitlist")
page("author.html", "The Author — KP Cap",
     "KP Cap — military spouse, world-builder since sixth grade, debut romantasy author. The Listening Dark was written between 2017 and her baby's nap times.",
     "author", AUTHOR, wl_target="#waitlist")
page("press.html", "Press Kit — The Listening Dark",
     "Press kit for The Listening Dark by KP Cap: fact sheet, boilerplate, assets, and enquiries.",
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
page("404.html", "Not Found — The Listening Dark",
     "The page you are listening for isn't here.", "", NOTFOUND, wl_target="index.html#waitlist")

print("\nDone. Built into:", ROOT)
