#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Writes the favicon set into the site root: favicon.svg, favicon.ico,
favicon-48.png, apple-touch-icon.png.

    python tools/make_favicons.py

Google only shows a favicon it can fetch as a real file, so a data: URI is not enough.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NIGHT, VIOLET, GOLD, MOON = "#141119", "#A78FE3", "#D2A85E", "#E6E3F2"

SVG = f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='{NIGHT}'/><circle cx='13' cy='14' r='8' stroke='{VIOLET}' stroke-width='1.4' fill='none' opacity='.9'/><circle cx='21' cy='20' r='4.5' fill='{GOLD}' opacity='.95'/><circle cx='24.5' cy='7.5' r='1.1' fill='{MOON}'/></svg>"""

def draw(size, rounded=True):
    # drawn at 16x then downsampled, pillow has no antialiasing of its own
    k = size * 16 / 32
    im = Image.new("RGBA", (size * 16, size * 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 32 * k - 1, 32 * k - 1), radius=6 * k if rounded else 0, fill=NIGHT)
    def circle(cx, cy, r, **kw):
        d.ellipse(((cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k), **kw)
    circle(13, 14, 8.7, outline=VIOLET, width=round(1.4 * k))
    circle(21, 20, 4.5, fill=GOLD)
    circle(24.5, 7.5, 1.1, fill=MOON)
    return im.resize((size, size), Image.LANCZOS)

with open(os.path.join(ROOT, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(SVG)
draw(48).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
draw(48).save(os.path.join(ROOT, "favicon-48.png"))
# ios rounds the corners itself and shows transparent ones as black
draw(180, rounded=False).convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"))
print("favicons written")
