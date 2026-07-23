# The Listening Dark — website

A premium pre-launch site for **The Listening Dark** by **KP Cap** — an **adult
fantasy romance (romantasy)**, Book One of a new series.
Plain **HTML / CSS / JS** — no build tools, no framework, no dependencies to install.

> Concept: *a violet night sky under twin moons.* Moonlight text, gold-foil and
> Danaya-violet accents, a static starfield, and the book's own words doing the
> selling — real Chapter One excerpt, real quotes, real bio. Calm by design:
> no flicker, no grain, comfortable contrast throughout.

## Drop-in assets (when ready)

| Asset | Where | What happens |
|---|---|---|
| Real cover art | `assets/cover.jpg` | Swap the typographic `.cover` mock in `tools/build.py` (`cover_block`) for `<img src="assets/cover.jpg" …>` |
| Author photo | `assets/author.jpg` | Open `author.html` (or `tools/build.py`), uncomment the ready-made `<img>` in the portrait `<figure>` |
| OG share image | `assets/og.png` (1200×630) | Add `og:image` / `twitter:image` meta in `tools/build.py` `head()` — **do this before launch**, shared links currently have no preview image |

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
| `book.html` | About the Book (synopsis, excerpt, themes, details) |
| `author.html` | About the Author (layout ready — bio blank) |
| `press.html` | Press Kit |
| `faq.html` | FAQ |
| `contact.html` | Contact |
| `privacy.html` · `terms.html` · `cookies.html` · `accessibility.html` | Legal |
| `404.html` | Not-found |

## Structure

```
index.html …            all pages (plain HTML, edit directly)
css/style.css           the entire design system + components
js/main.js              all behaviour (nav, menu, grain, reveals, forms)
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

Real content is now live: Chapter One excerpt, quotes, synopsis, author bio,
dedication, socials (@kpcapitulo / @kp.capitulo), genre & content notes.
Still to do:

- **Cover art** and **author photo** (see drop-in table above)
- **OG share image** — without it, links shared to Instagram/TikTok/iMessage show no preview
- **Book details** as they firm up (formats, page count, ISBN, publication date)
- **Press kit downloads** (currently "coming soon" cards)
- **Legal copy** (drafts in place — review with counsel)

## Wire up the forms (important)

The waitlist and contact forms are **front-end demos** — they validate and show a
success message but **don't send anything yet**. To make them live, connect them
to an email service. Easiest options for an author:

- **Kit (ConvertKit)** or **Beehiiv** — newsletter-native, free tier, own your list.
- **Formspree** / **Netlify Forms** — for the contact form, near-zero setup.

In `js/main.js`, the form handlers are marked
`/* demo — wire to an ESP for production */` — replace the success block with a
`fetch()` POST to your provider (or add the provider's `action`/attributes to the
`<form>` tags).

---

## Design notes

- **Deliberately dark-only** — a committed nocturnal world; the theme toggle is intentionally ignored.
- **Accessible** — keyboard-navigable, visible focus, honours `prefers-reduced-motion`
  (grain, parallax, cursor, and reveals all switch off), semantic structure.
- **Fast** — fonts are local & subset; no external requests; works offline.
- Full design rationale lives in the approved design plan.
