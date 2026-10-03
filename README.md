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

Drag-and-drop the whole folder to any static host — no configuration needed:

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

## Structure

```
index.html …            all pages (plain HTML, edit directly)
css/style.css           the entire design system + components
js/main.js              all behaviour (nav, menu, reveals, forms)
assets/fonts/           Fraunces · Newsreader · Inter · Space Mono (local .woff2)
tools/build.py          optional generator — regenerates the HTML from shared
                        nav/footer fragments so they never drift. NOT required
                        to run the site.
```

> **Editing tip:** the nav bar and footer are identical on every page. If you
> change them, **edit `tools/build.py` and re-run `python tools/build.py`** —
> treat the HTML files as generated output. (Hand-edits to the HTML will be
> silently overwritten the next time the generator runs.)

---

## Before launch — what's left

Real content is now live: the official back-cover synopsis, quotes, author bio,
dedication, socials (@kpcapitulo / @kp.capitulo), genre & content notes.
Still to do:

- **Book details** as they firm up (formats, page count, ISBN, publication date)
- **Press kit downloads** (currently "coming soon" cards)
- **Legal copy** (drafts in place — review with counsel)

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
