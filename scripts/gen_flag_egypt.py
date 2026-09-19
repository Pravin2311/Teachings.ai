"""
learn/country/egypt.html referenced assets/images/flags/egypt.png, which
never existed -- unlike the wildlife/fruit/vehicle-part icons, a flag is
factual geographic content, so this deliberately does NOT go through the
generic emoji-badge generator (a purple circle with "FO" in it would be
actively wrong for "this is Egypt's flag", worse than leaving it broken).

Draws the real flag: three equal horizontal bands, red/white/black, per
the actual Flag of Egypt. Skips the Eagle of Saladin emblem in the
center band (a common simplification in kids' educational flag charts)
rather than risk drawing it inaccurately.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "images", "flags", "egypt.png")

W, H = 300, 200
RED = (206, 17, 38)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    band = H // 3
    draw.rectangle([0, 0, W, band], fill=RED)
    draw.rectangle([0, band, W, band * 2], fill=WHITE)
    draw.rectangle([0, band * 2, W, H], fill=BLACK)
    img.save(OUT, quality=90)
    print(f"Wrote {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
