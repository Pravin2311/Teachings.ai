"""
learn/country/australia.html referenced <img src="/assets/images/flags/">
-- an empty path (missing filename entirely), and no Australia flag file
exists at any name. Like Egypt, this is factual geographic content, so it
gets a real, geometrically-correct flag rather than a generic badge.

Draws: navy blue field, the Union Jack in the canton (top-left quarter),
the 7-pointed Commonwealth Star below it, and the Southern Cross on the
fly half (4 seven-pointed stars + 1 smaller five-pointed star) --
matching the real flag's actual layout and star points.
"""
import os
import math
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "images", "flags", "Australia.png")

W, H = 300, 150
NAVY = (0, 30, 92)
RED = (204, 20, 43)
WHITE = (255, 255, 255)


def star_points(cx, cy, r_outer, r_inner, n, rotation=-math.pi / 2):
    pts = []
    for i in range(n * 2):
        r = r_outer if i % 2 == 0 else r_inner
        angle = rotation + i * math.pi / n
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


def draw_star(draw, cx, cy, r_outer, points=7, fill=WHITE):
    r_inner = r_outer * 0.42
    draw.polygon(star_points(cx, cy, r_outer, r_inner, points), fill=fill)


def draw_union_jack(img, x0, y0, cw, ch):
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=NAVY)
    # white diagonals (St Andrew's cross ground)
    band = max(2, int(ch * 0.14))
    d.line([(x0, y0), (x0 + cw, y0 + ch)], fill=WHITE, width=band)
    d.line([(x0 + cw, y0), (x0, y0 + ch)], fill=WHITE, width=band)
    # red diagonals (St Patrick's cross), offset
    band_r = max(1, int(ch * 0.07))
    d.line([(x0, y0), (x0 + cw, y0 + ch)], fill=RED, width=band_r)
    d.line([(x0 + cw, y0), (x0, y0 + ch)], fill=RED, width=band_r)
    # white cross (St George's ground)
    band_w = max(2, int(ch * 0.22))
    d.rectangle([x0 + cw / 2 - band_w / 2, y0, x0 + cw / 2 + band_w / 2, y0 + ch], fill=WHITE)
    d.rectangle([x0, y0 + ch / 2 - band_w / 2, x0 + cw, y0 + ch / 2 + band_w / 2], fill=WHITE)
    # red cross (St George's cross), narrower
    band_rw = max(1, int(ch * 0.11))
    d.rectangle([x0 + cw / 2 - band_rw / 2, y0, x0 + cw / 2 + band_rw / 2, y0 + ch], fill=RED)
    d.rectangle([x0, y0 + ch / 2 - band_rw / 2, x0 + cw, y0 + ch / 2 + band_rw / 2], fill=RED)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    canton_w, canton_h = W * 0.5, H * 0.5
    draw_union_jack(img, 0, 0, canton_w, canton_h)

    draw = ImageDraw.Draw(img)
    # Commonwealth Star: 7 points, below the canton
    draw_star(draw, canton_w * 0.5, canton_h * 1.28, H * 0.11, points=7)

    # Southern Cross on the fly (right) half -- real relative positions
    draw_star(draw, W * 0.62, H * 0.22, H * 0.10, points=7)   # Alpha
    draw_star(draw, W * 0.86, H * 0.38, H * 0.10, points=7)   # Beta
    draw_star(draw, W * 0.90, H * 0.68, H * 0.10, points=7)   # Gamma
    draw_star(draw, W * 0.72, H * 0.82, H * 0.10, points=7)   # Delta
    draw_star(draw, W * 0.76, H * 0.56, H * 0.055, points=5)  # Epsilon (smaller)

    img.save(OUT, quality=90)
    print(f"Wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
