#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates the hero's twin-moon artwork: assets/moons.webp.

Everything here is synthesised from seeded noise - the crater field, the
rim light, the smoke. No source photograph is sampled, so the output is
original artwork and safe to publish. Re-run with a different SEED to get
a different moon; the composition stays put.

    python tools/make_moons.py

Palette is pinned to the site tokens: violet-grey regolith, #D2A85E rim
light, #E6E3F2 for the brightest specks.
"""
import os
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "moons.webp")

SEED = 20260928
SS = 2                      # supersample factor, downscaled at the end
W = H = 1100 * SS
rng = np.random.default_rng(SEED)

# site tokens
GOLD = np.array([210, 168, 94]) / 255.0
MOONLIGHT = np.array([230, 227, 242]) / 255.0
REGOLITH = np.array([0.62, 0.60, 0.68])   # tinted violet, darkened later
SMOKE_RGB = np.array([18, 16, 24]) / 255.0


def fbm(shape, octaves=6, lac=2.0, gain=0.5, base=4.0):
    """Fractal noise built from smoothed white noise, normalised to 0..1."""
    out = np.zeros(shape, dtype=np.float32)
    amp, freq, norm = 1.0, base, 0.0
    for _ in range(octaves):
        # a small random field blown up and smoothed is a cheap value-noise octave
        small = rng.random((max(2, int(freq)), max(2, int(freq)))).astype(np.float32)
        layer = np.array(Image.fromarray((small * 255).astype(np.uint8))
                         .resize((shape[1], shape[0]), Image.BICUBIC), dtype=np.float32) / 255.0
        out += amp * layer
        norm += amp
        amp *= gain
        freq *= lac
    out /= norm
    return (out - out.min()) / max(1e-6, out.ptp())


def crater_field(size, count, rmin, rmax, seed_shift=0):
    """Height map of overlapping craters: depressed floor, raised rim.

    Sizes follow a power law so there are many small craters and few large
    ones, which is what stops a procedural moon looking like golf balls.
    """
    g = np.random.default_rng(SEED + seed_shift)
    h = np.zeros((size, size), dtype=np.float32)
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    for _ in range(count):
        r = rmin * (rmax / rmin) ** (g.random() ** 1.9)
        cx, cy = g.random() * size, g.random() * size
        pad = int(r * 2.2)
        x0, x1 = max(0, int(cx - pad)), min(size, int(cx + pad))
        y0, y1 = max(0, int(cy - pad)), min(size, int(cy + pad))
        if x1 <= x0 or y1 <= y0:
            continue
        d = np.sqrt((xx[y0:y1, x0:x1] - cx) ** 2 + (yy[y0:y1, x0:x1] - cy) ** 2) / r
        floor = -np.exp(-(d ** 2) * 1.9)          # bowl
        rim = 1.30 * np.exp(-((d - 1.0) ** 2) * 11.0)  # raised ring at d=1
        depth = 0.45 + 0.75 * g.random()
        h[y0:y1, x0:x1] += (floor + rim) * depth * (r ** 0.55)
    return h


def render_moon(size, radius_px, fill, rim_dir, seed_shift, crater_count):
    """One sphere: (rgb, alpha).

    Two light terms, because one cannot do both jobs. `fill` is a dim frontal
    light whose only purpose is to make the crater field readable. `rim_dir`
    is the warm backlight that produces the gold limb - it is what the eye
    actually reads as "moon".
    """
    y, x = np.mgrid[0:size, 0:size].astype(np.float32)
    cx = cy = (size - 1) / 2.0
    nx = (x - cx) / radius_px
    ny = (y - cy) / radius_px
    r2 = nx ** 2 + ny ** 2
    inside = r2 <= 1.0
    nz = np.sqrt(np.clip(1.0 - r2, 0.0, 1.0))

    # --- surface relief: broad maria plus the crater field ---
    # A flat texture pasted on a disc looks flat, so sample it through
    # tx = nx / (a + b*nz) to compress detail toward the limb. Keep the
    # divisor well away from zero or the sampling smears into radial streaks.
    warp = 0.62 + 0.38 * nz
    tx = np.clip(cx + (nx / warp) * radius_px, 0, size - 1)
    ty = np.clip(cy + (ny / warp) * radius_px, 0, size - 1)
    limb_fade = nz ** 0.42          # relief flattens out as the surface turns away

    maria_raw = fbm((size, size), octaves=5, base=3.0)
    craters_raw = crater_field(size, crater_count, 4.5 * SS, 82.0 * SS, seed_shift)
    craters_raw = gaussian_filter(craters_raw, 0.6 * SS)
    craters_raw /= max(1e-6, np.abs(craters_raw).max())

    maria = map_coordinates(maria_raw, [ty, tx], order=1, mode='reflect')
    craters = map_coordinates(craters_raw, [ty, tx], order=1, mode='reflect')
    relief = (0.26 * (maria - 0.5) + 1.00 * craters) * limb_fade

    # perturb the sphere normal by the relief gradient (bump mapping)
    gy, gx = np.gradient(relief.astype(np.float32))
    bump = 16.0
    Nx, Ny, Nz = nx - bump * gx, ny - bump * gy, nz + 1e-6
    ln = np.sqrt(Nx ** 2 + Ny ** 2 + Nz ** 2)
    Nx, Ny, Nz = Nx / ln, Ny / ln, Nz / ln

    F = np.array(fill, dtype=np.float32); F /= np.linalg.norm(F)
    diffuse = np.clip(Nx * F[0] + Ny * F[1] + Nz * F[2], 0.0, 1.0)

    # the maria are genuinely dark basalt plains, not a gentle gradient
    plains = np.clip((maria - 0.44) * 3.6, 0.0, 1.0)
    albedo = 0.30 + 0.52 * plains
    albedo *= 0.86 + 0.28 * map_coordinates(
        fbm((size, size), octaves=4, base=11.0), [ty, tx], order=1, mode='reflect')

    shade = 0.055 + 0.62 * (diffuse ** 1.25) * albedo
    rgb = shade[..., None] * REGOLITH[None, None, :]

    # --- warm limb light from rim_dir: fresnel, gated to that side ---
    R = np.array(rim_dir, dtype=np.float32); R /= np.linalg.norm(R)
    fres = np.clip(1.0 - nz, 0.0, 1.0) ** 4.2
    rim_side = np.clip(nx * R[0] + ny * R[1], 0.0, 1.0) ** 0.75
    rim = fres * (0.10 + 1.95 * rim_side)
    rgb += (rim * 1.22)[..., None] * GOLD[None, None, :]

    # a thin crescent exactly at the edge sells the sphere
    edge = np.exp(-((np.sqrt(r2) - 0.986) ** 2) / (2 * 0.009 ** 2))
    rgb += (edge * rim_side * 0.95)[..., None] * GOLD[None, None, :]

    # sparse bright specks, brighter where the fill already hits
    sp = np.random.default_rng(SEED + 77 + seed_shift).random((size, size))
    specks = (sp > 0.99996).astype(np.float32) * (0.30 + 0.70 * diffuse)
    specks = gaussian_filter(specks, 0.5 * SS) * 6.0
    rgb += specks[..., None] * MOONLIGHT[None, None, :]

    alpha = gaussian_filter(inside.astype(np.float32), 0.7 * SS)
    rgb *= alpha[..., None]
    return np.clip(rgb, 0, 1), alpha


def smoke_layer(shape, moon_mask, centre, spread):
    """Ridged, domain-warped noise held in an annulus around the moons.

    Plain fbm reads as cloud. Folding it (1 - |2n-1|) puts a crease along
    every zero crossing, and those creases are what look like tendrils.
    """
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    q = fbm(shape, octaves=5, base=6.0)
    r = fbm(shape, octaves=5, base=9.0)
    amp = 190.0 * SS
    cxw = np.clip(xx + amp * (q - 0.5), 0, w - 1)
    cyw = np.clip(yy + amp * (r - 0.5), 0, h - 1)

    field = fbm(shape, octaves=7, base=7.0)
    ridged = 1.0 - np.abs(2.0 * field - 1.0)
    warped = map_coordinates(ridged, [cyw, cxw], order=1, mode="reflect")

    d = np.sqrt((xx - centre[0]) ** 2 + (yy - centre[1]) ** 2) / spread
    # tight annulus: the smoke has to hug the pair. Widen this and it stops
    # reading as smoke and starts reading as marble.
    halo = np.exp(-((d - 0.44) ** 2) / (2 * 0.17 ** 2))
    a = np.clip((warped - 0.74) * 4.6, 0, 1) ** 1.05 * halo
    a = gaussian_filter(a, 0.9 * SS)
    # hard fade before the canvas edge so nothing looks cropped
    ex = np.maximum(np.abs(xx - w / 2) / (w / 2), np.abs(yy - h / 2) / (h / 2))
    a *= np.clip((0.97 - ex) / 0.22, 0, 1)
    # thin the smoke where it crosses a moon so the disc stays readable
    a *= (1.0 - 0.62 * moon_mask)
    return np.clip(a * 1.05, 0, 1)


def paste(dst_rgb, dst_a, src_rgb, src_a, ox, oy):
    """Source-over composite of a square tile at (ox, oy)."""
    sh, sw = src_a.shape
    x0, y0 = max(0, ox), max(0, oy)
    x1, y1 = min(dst_a.shape[1], ox + sw), min(dst_a.shape[0], oy + sh)
    if x1 <= x0 or y1 <= y0:
        return
    sx0, sy0 = x0 - ox, y0 - oy
    s_rgb = src_rgb[sy0:sy0 + (y1 - y0), sx0:sx0 + (x1 - x0)]
    s_a = src_a[sy0:sy0 + (y1 - y0), sx0:sx0 + (x1 - x0)]
    d_rgb = dst_rgb[y0:y1, x0:x1]
    d_a = dst_a[y0:y1, x0:x1]
    out_a = s_a + d_a * (1 - s_a)
    dst_rgb[y0:y1, x0:x1] = s_rgb + d_rgb * (1 - s_a)[..., None]
    dst_a[y0:y1, x0:x1] = out_a


def main():
    rgb = np.zeros((H, W, 3), dtype=np.float32)
    alpha = np.zeros((H, W), dtype=np.float32)

    # the far moon sits upper-left and is lit from its lower-right, so the
    # warm light reads as coming from between the pair
    r_far = int(0.215 * W)
    tile_far = r_far * 2 + 40 * SS
    far_rgb, far_a = render_moon(tile_far, r_far,
                                 fill=(0.30, 0.10, 0.95), rim_dir=(0.80, 0.60, 0.20),
                                 seed_shift=11, crater_count=380)
    far_x, far_y = int(0.155 * W), int(0.120 * H)

    r_near = int(0.232 * W)
    tile_near = r_near * 2 + 40 * SS
    near_rgb, near_a = render_moon(tile_near, r_near,
                                   fill=(-0.18, -0.12, 0.97), rim_dir=(-0.62, -0.52, 0.20),
                                   seed_shift=29, crater_count=460)
    near_x, near_y = int(0.365 * W), int(0.400 * H)

    moon_mask = np.zeros((H, W), dtype=np.float32)
    m_tmp_rgb = np.zeros((H, W, 3), dtype=np.float32)
    paste(m_tmp_rgb, moon_mask, np.zeros_like(far_rgb), far_a, far_x, far_y)
    paste(m_tmp_rgb, moon_mask, np.zeros_like(near_rgb), near_a, near_x, near_y)

    centre = ((far_x + tile_far / 2 + near_x + tile_near / 2) / 2,
              (far_y + tile_far / 2 + near_y + tile_near / 2) / 2)
    smoke_a = smoke_layer((H, W), moon_mask, centre, 0.60 * W)
    smoke_rgb = np.broadcast_to(SMOKE_RGB, (H, W, 3)).astype(np.float32) * smoke_a[..., None]
    rgb, alpha = smoke_rgb.copy(), smoke_a.copy()

    # glow in the contact zone, painted before the near moon so the near
    # moon's dark limb occludes it
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    seam = np.exp(-(((xx - 0.455 * W) ** 2 + (yy - 0.415 * H) ** 2) / (2 * (0.145 * W) ** 2)))
    paste(rgb, alpha, (seam * 0.55)[..., None] * GOLD[None, None, :],
          np.clip(seam * 0.50, 0, 1), 0, 0)

    paste(rgb, alpha, far_rgb, far_a, far_x, far_y)
    paste(rgb, alpha, near_rgb, near_a, near_x, near_y)

    out = np.concatenate([np.clip(rgb, 0, 1), np.clip(alpha, 0, 1)[..., None]], axis=2)
    img = Image.fromarray((out * 255 + 0.5).astype(np.uint8), mode="RGBA")
    img = img.resize((W // SS, H // SS), Image.LANCZOS)
    # WebP with alpha: ~5x smaller than PNG here (149 KB vs 722 KB) with no
    # visible difference on a dark ground. Every browser that supports the
    # CSS this site already uses supports WebP.
    img.save(OUT, "WEBP", quality=86, method=6)
    kb = os.path.getsize(OUT) / 1024
    print("wrote %s  %sx%s  %.0f KB" % (OUT, img.width, img.height, kb))


if __name__ == "__main__":
    main()
