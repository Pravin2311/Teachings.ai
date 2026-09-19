"""
Generates real, on-brand 1200x630 OG/Twitter preview images for the ~28
pages that were falling back to the generic app_icon_512.png logo after
the broken-og-image fix. A square logo thumbnail is a weak search/social
result compared to a proper landscape preview card naming the topic --
this closes that gap without needing hand-made art.

Uses the site's own brand palette (--head:#1B2A5B / --brand:#2b5cff /
--accent:#ffb300, taken from index.html's own CSS custom properties) and
Poppins (the site's own heading font, confirmed installed locally) so
these read as genuinely on-brand rather than generic stock cards.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "images", "og")
FONT_DIR = "C:/Windows/Fonts"

NAVY = (27, 42, 91)       # #1B2A5B
NAVY_DEEP = (16, 26, 59)  # darker shade for gradient
BLUE = (43, 92, 255)      # #2b5cff
AMBER = (255, 179, 0)     # #ffb300
WHITE = (255, 255, 255)
W, H = 1200, 630

CARDS = {
    "vegetables": "Vegetables",
    "alphabets": "Alphabets A-Z",
    "countries": "Countries of the World",
    "worksheet-cover": "Free Printable Worksheets",
    "electronic-gadgets": "Electronic Gadgets",
    "fantasy-characters": "Fantasy World",
    "alphabet-collection": "Alphabets A-Z",
    "animal-collection": "Animals",
    "bird-collection": "Birds",
    "body-collection": "Body Parts",
    "rainbow-collage": "Colors",
    "world-map-collage": "Countries of the World",
    "tech-collage": "Electronics",
    "fruit-basket-collage": "Fruits",
    "learning-hub-banner": "World of Learning",
    "solar-system-collage": "Planets & Space",
    "veggie-basket-collage": "Vegetables",
    "vehicle-collage": "Vehicles",
    "odd-even-preview": "Odd & Even Numbers",
    "planets-preview": "Planets & Space",
    "plants-cover": "Plants",
    "publicservice-preview": "Community Helpers",
    "rhyming-preview": "Rhyming Words",
    "scientists-preview": "Great Scientists",
    "shapes-cover": "Shapes",
    "sight-words-preview": "Sight Words",
    "vehicles-preview": "Vehicles",
    "word-matching-preview": "Word Matching",
}

TAGLINE = "Free Learning Games for Kids  \u00b7  teachings.ai"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_card(title, out_path):
    img = Image.new("RGB", (W, H), NAVY)
    px = img.load()
    for y in range(H):
        t = y / H
        c = lerp(NAVY, NAVY_DEEP, t)
        for x in range(W):
            px[x, y] = c

    draw = ImageDraw.Draw(img)

    # soft accent shapes -- kept spatially separate so colors never mix muddy
    draw.ellipse([W - 460, -220, W + 80, 400], fill=lerp(BLUE, NAVY, 0.3))
    for i, r in enumerate([26, 18, 12]):
        cx, cy = W - 90 - i * 54, H - 90
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=lerp(AMBER, NAVY, 0.15))

    # left accent bar
    draw.rectangle([0, 0, 14, H], fill=AMBER)

    # wordmark, top-left
    wordmark_font = ImageFont.truetype(f"{FONT_DIR}/Poppins-Bold.ttf", 34)
    draw.text((70, 60), "Teachings", font=wordmark_font, fill=WHITE)
    bbox = draw.textbbox((70, 60), "Teachings", font=wordmark_font)
    draw.text((bbox[2] + 4, 60), ".ai", font=wordmark_font, fill=AMBER)

    # title, auto-shrink to fit width
    max_width = W - 140
    size = 92
    title_font = ImageFont.truetype(f"{FONT_DIR}/Poppins-Bold.ttf", size)
    while True:
        bbox = draw.textbbox((0, 0), title, font=title_font)
        tw = bbox[2] - bbox[0]
        if tw <= max_width or size <= 44:
            break
        size -= 4
        title_font = ImageFont.truetype(f"{FONT_DIR}/Poppins-Bold.ttf", size)
    th = bbox[3] - bbox[1]
    tx = 70
    ty = (H - th) // 2 - 10
    draw.text((tx, ty), title, font=title_font, fill=WHITE)

    # underline accent
    draw.rectangle([tx, ty + th + 26, tx + 90, ty + th + 34], fill=AMBER)

    # tagline
    tag_font = ImageFont.truetype(f"{FONT_DIR}/Poppins-Regular.ttf", 30)
    draw.text((70, H - 90), TAGLINE, font=tag_font, fill=(210, 218, 240))

    img.save(out_path, quality=90)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    only = sys.argv[1] if len(sys.argv) > 1 else None
    made = []
    for slug, title in CARDS.items():
        if only and slug != only:
            continue
        out_path = os.path.join(OUT_DIR, f"{slug}.jpg")
        make_card(title, out_path)
        made.append(out_path)
    print(f"Generated {len(made)} card(s):")
    for p in made:
        print(f"  {os.path.relpath(p, ROOT)}")


if __name__ == "__main__":
    main()
