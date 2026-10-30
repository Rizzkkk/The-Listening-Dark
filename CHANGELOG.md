# Changelog

## Deploying

Server details and the deploy one-liner live in `DEPLOY.local.md`, which is
gitignored because this repo is public.

---

## 2026-10-30

Publication day. Ordering is now visible from more than one spot:

- **Get your copy.** A new block puts Kindle and the signed copy side by side.
  - Where: on the home page (in place of the old "The Kindle edition is available" strip) and on The Book page after The Story. The Book page had no way to buy a signed copy before.
  - What the signed half shows: it comes from a tenth fragment, `book-buy`.
    - open: price, shipping and copies left, with an "Order a signed copy" button that goes to the order card;
    - sold out: "Sold out" and a waitlist link;
    - closed, or with the service down: "Opens soon" and a waitlist link.
  - Styles are `.get-copy` and `.buy-*` in `css/style.css`; the unused `.soft-ask` rules are gone.
- **Closed state.** The order area under `#signed` now says "Signed copies open soon. Leave your email..." under the pill, instead of only "check back soon".
- **Kindle is out.** `PRE_ORDER = False`: every Kindle button says "Buy on Kindle", the structured data says `InStock`, and the FAQ sample answer no longer says "once it is out".
- **Checks.** `check_site.py` is now 100/100. It checks that both pages show the block in every state, with an order link only while open. Fixtures regenerated.

## 2026-10-29

How a buyer orders is now one clear path:

- **Order card.** The `signed-cta` fragment (from the store service) is now a card:
  - price and copies left;
  - copies as radio pills;
  - Book, shipping and Total lines;
  - a tucked-away "Have a discount code?" box, shown only when shipping costs money;
  - a gold "Continue to secure checkout" button and a trust line.

  `js/main.js` keeps the total in step with the copies picked (display only; checkout recomputes every amount). It also disables the button after one tap, so a double tap can't open two Stripe pages. The styles are `.order-card` in `css/style.css`. The old `.signed-form` rules stay for one release.
- **Spec list.** `signed-spec` drops Price and Availability while the card shows, since the card has both.
- **Menu link.** "Signed copy" is in the desktop menu and the mobile menu through a ninth fragment, `nav-signed`. It shows only while the shop is open. Closed, sold out, or with the service down, every page is exactly what it was without the shop; `check_site` S3 still proves that byte for byte.
- **Dedications.** Buyers can give an optional name to sign the copy to, on the Stripe page. The thank-you page mentions it, the terms say it's signed exactly as typed, and the privacy page lists it.
- **Short link.** `kpcapitulo.com/signed` redirects to the card. That's an nginx rule in the store repo.
- **Checks.** `check_site.py` 91/91. Fixtures regenerated for the new contract.

## 2026-10-28

Signed copies switched on: `SHOP_ENABLED = True`. The site now ships `thank-you.html`
and `checkout-unavailable.html` (a paid test checkout had landed on a 404), the
"Signed copies" terms, and the order sections in privacy and cookies. Until the server
includes the live values, every signed-copy spot shows its "check back soon" fallback.

- The order form gains an optional "Discount code" box when the store's free-shipping
  code is switched on. The code word itself never appears in the page.
- Order emails are now sent through Brevo (privacy page updated).
- `tools/check_site.py` forces the switch both ways itself, so it checks the off and on
  builds whatever the file says.

---

## 2026-10-10

Signed-copy support, switched off. Everything below is built and tested, and nothing
signed-copy-related is public: the new switch is `False`. (This replaces the same-day
first version, which used a fixed Payment Link and a seller-disclosure page; that page
and its constants are gone.)

- One switch at the top of `tools/build.py`, `SHOP_ENABLED`, replaces the earlier
  constants (`CHECKOUT_URL`, `SOLD_OUT`, `SIGNED_APPROVED`, `LEGAL_NAME`,
  `SIGNED_FORMAT`, `SIGNED_COPIES`, `SIGNED_SHIPPING`, `RETURNS_TEXT`). It is the
  author's sign-off. Off builds the site with no signed-copy sales machinery. On adds
  the pieces below. The price, ship window and record-keeping wording stay as constants
  (`PRICE_USD`, `SIGNED_SHIPS`, `RETENTION`).
- Live values (price line, stock, order button, refund policy, the signed edition in
  the structured data) come from a separate service and reach the pages as server-side
  includes. `ssi(name, fallback)` wraps each of eight places in an include point with a
  built-in fallback, and stops the build on an unknown name. If the service or an
  include is missing, or the page is opened locally, the fallback shows: the signed-copy
  area reads "check back soon" and nothing breaks.
- With `SHOP_ENABLED` on, the build also adds a "Signed copies" section to the terms,
  an orders section to the privacy policy, a checkout section to the cookie policy,
  `thank-you.html` and `checkout-unavailable.html` (both `noindex`, not in the sitemap;
  neither claims a payment went through). `404.html` and these pages share `page()`'s
  `listed=False`, which skips the canonical tag and sitemap entry.
- The closed copy changed on the default build: the pill now reads "Signed author's
  copy · check back soon" (it was "coming soon", which stops being true after a first
  run), the FAQ says signed copies "aren't on sale right now", and the spec's shipping
  row reads "USPS, US and APO/FPO/DPO". These three phrases are the only visible
  differences from the 2026-10-06 build with the switch off.
- If a shop page or `commerce-disclosure.html` is left over from an earlier build, the
  build deletes it and prints "removed ...". Commit that deletion, or the deploy pull
  leaves the old page live.
- JSON-LD escapes `<`, so no value can close the script block early.
- `tools/check_site.py`: builds patched copies of the site in temp folders and checks
  five scenarios (shop off, shop on, includes emulated with their fallbacks, includes
  emulated with sample fragments from `tools/fixtures/shop/`, build guards), 89 checks.
  It never touches the repo's HTML. Run `python tools/check_site.py`; add `--keep` to
  keep the temp builds.
- `tools/hooks/pre-commit` blocks commits containing Stripe secret, restricted or
  webhook key patterns, private keys, `.env` files, `.db`/`.sqlite`/`.csv` files,
  `DEPLOY.local.md` or the private planning folder. Each clone enables it once with
  `git config core.hooksPath tools/hooks`.
- `.gitignore` now also covers `.env*`, databases, `*.csv`, `orders/`, `backups/`,
  `DEPLOY.local.md` and the private planning folder.

**Turning it on** (not scheduled): the live values need the separate service and a web
server with includes enabled. Set `SHOP_ENABLED = True`, run
`python tools/check_site.py`, run `python tools/build.py`, commit (including any
deleted pages), deploy. To back out, set it to `False` and deploy.

## 2026-10-06

- Hero second button is now the signed author's copy instead of the print/Book
  Two signup. It pointed at a `SHOPIFY_URL` constant in `tools/build.py`; while
  that was empty it rendered as a non-clickable "coming soon" pill rather than a
  dead link. The Shopify plan was dropped before launch: `SHOPIFY_URL` was
  removed, and the button follows the `SHOP_ENABLED` switch (see 2026-10-10).
- New home section (`#signed`) after the Kindle soft-ask: the $22 signed-copy
  poster (`assets/signed-copy.jpg`) with price, shipping and availability. Its
  button follows the same switch. The FAQ paperback answer links to it.
- Favicon is now real files in the site root (`favicon.ico`, `favicon.svg`,
  `favicon-48.png`, `apple-touch-icon.png`), generated by
  `python tools/make_favicons.py`. The old inline `data:` icon was invisible to
  Google, which is why search results showed a blank globe.

## 2026-10-03

Kindle is now the primary call to action; the waitlist stays as a secondary list.

- Nav, mobile menu and hero buttons go to the Kindle page (`KINDLE_URL`). The
  hero keeps a second button down to the signup.
- The signup is reworded for print editions and Book Two ("Notify Me"); the
  FormSubmit subject is now "Updates signup". FAQ gains a paperback question,
  and the sample answer points at Amazon's "Read sample".
- Privacy and terms wording updated to match; Amazon added to third-party links.
- `og:image` is now an absolute URL (social previews ignored the relative one),
  plus `og:url` and `<link rel="canonical">` on every page except 404.
- `robots.txt` and `sitemap.xml` are generated by `tools/build.py`.
- Book JSON-LD on index and book pages.

**Release day (Oct 30):** set `PRE_ORDER = False` at the top of `tools/build.py`,
run `python tools/build.py`, commit, deploy. That flips every "Pre-order on
Kindle" to "Buy on Kindle" and the JSON-LD availability to InStock.

## 2026-10-01

- Publication date set to **October 30, 2026** (`PUB_DATE` in `tools/build.py`):
  home hero, home and book details, author timeline, FAQ.
- The home page "cover reveal" waitlist card now links to the Kindle pre-order
  (`KINDLE_URL`). Book details list the format as Kindle eBook.
- The waitlist itself (nav button, bottom section, footer form) is unchanged.

## 2026-09-29 — `f26ef22`

- Removed the Chapter One excerpt everywhere: the `#excerpt` sections, the hero
  "Read Chapter One" button, the footer links on all 11 pages, the meta
  descriptions and the terms.html excerpt clauses. The FAQ sample question now
  points at the waitlist.
- Replaced the synopsis with the official back-cover copy on index and book.
- Emptied the press kit down to a "coming soon" note pending approved assets.
- Removed the comp titles ("ACOTAR energy, Throne of Glass pacing").

Dead `.reading` / `.gate` / `.dropcap` CSS and the `[data-unlock]` handler went
with it.

## 2026-09-28 — `c478868`

Home page rebuilt from the Claude Design handoff, plus the new cover.

- New section order: hero, premise, story, soft ask, pull-quote, author,
  waitlist. Stacked hero title, staged cover with an offset gold frame,
  arch-cropped author portrait.
- Site-wide: buttons and text links moved to sentence case (uppercase tracking
  is now reserved for kickers and meta), nav links to 14px, and the waitlist
  band became full-bleed with a real field label instead of an `aria-label`.
- Cover replaced with the front panel of the new spread (900×1333). Its alt
  text described the previous artwork and was rewritten. OG card rebuilt.
- Hero moons generated by `tools/make_moons.py` — craters, rim light and smoke
  synthesised from seeded noise, so the image is original. 149 KB WebP.
- Author photo added.

Fixes: the base `img` rule was missing `height:auto`, so images carrying
`width`/`height` attributes rendered at full intrinsic height; a light mockup
sliver was cropped off the old cover; the cover stage now derives its height
from the image rather than a hardcoded `aspect-ratio`; the spec strip no longer
keeps an orphaned left rule when it wraps.

Quotes were checked against the beta manuscript. Two lines were blurb copy that
appears nowhere in the book — the hero tagline and a stitched pull-quote
presented as the book's own voice. Both replaced with verbatim text, and the
pull-quote is now cited to Dezi.

## 2026-07-23 — `73820e8`

Initial commit.
