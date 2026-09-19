"""
audit_broken_content_images.py found 143 broken in-page <img> references
across 28 pages (mostly learn/country/*.html wildlife icons, plus fruit/
vegetable variety icons and vehicle-parts diagrams on a few learn/ pages)
-- these render as visibly broken image icons on live pages right now,
which directly hurts trust and time-on-page for the exact audience
(parents, teachers, kids) this site exists for.

Generates a real, consistent 240x240 icon badge per broken filename
(displayed at the existing 70x70 via each <img>'s own width/height --
rendered larger for retina sharpness). Label text comes straight from
each image's own alt attribute (already accurate, e.g. "Purple Carrot",
"Periscope") rather than being hand-typed per file. A small keyword
lookup picks a matching emoji where one exists and is genuinely
recognizable; falls back to the label's initial letters (clean
typographic mark) rather than forcing a wrong or misleading emoji onto
something like "Periscope" or "Sonar".
"""
import os
import re
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
FONT_DIR = "C:/Windows/Fonts"
SIZE = 240

# brand-derived palette, cycled by hash of the filename so nearby icons in
# the same grid get visual variety without being random/inconsistent
PALETTE = [
    (43, 92, 255),    # brand blue
    (27, 42, 91),     # navy
    (255, 152, 0),    # warm orange
    (15, 138, 75),    # green
    (199, 42, 42),    # red
    (124, 58, 195),   # purple
]

EMOJI_MAP = [
    (("grizzly", "brown bear", "polar bear", "bear"), "\U0001F43B"),
    (("panda",), "\U0001F43C"),
    (("moose", "caribou", "deer", "elk"), "\U0001F98C"),
    (("wolf", "jackal", "fox"), "\U0001F43A"),
    (("leopard", "jaguar", "cheetah", "tiger", "lynx"), "\U0001F406"),
    (("rhino",), "\U0001F98F"),
    (("crocodile", "alligator"), "\U0001F40A"),
    (("buffalo", "bison"), "\U0001F403"),
    (("cow",), "\U0001F404"),
    (("hippo",), "\U0001F99B"),
    (("gorilla",), "\U0001F98D"),
    (("monkey", "macaque",), "\U0001F412"),
    (("eagle",), "\U0001F985"),
    (("crane", "flamingo", "ibis"), "\U0001F9A9"),
    (("pheasant", "rooster"), "\U0001F413"),
    (("kookaburra", "toucan", "macaw", "parrot"), "\U0001F99C"),
    (("koala",), "\U0001F428"),
    (("wombat", "beaver", "marmot", "raccoon dog", "tanuki", "capybara"), "\U0001F994"),
    (("platypus", "loon", "duck"), "\U0001F986"),
    (("emu", "dingo",), "\U0001F995"),
    (("dolphin",), "\U0001F42C"),
    (("anaconda", "cobra", "snake"), "\U0001F40D"),
    (("walrus", "seal"), "\U0001F9AD"),
    (("camel", "dromedary"), "\U0001F42B"),
    (("scorpion",), "\U0001F982"),
    (("chamois", "goat"), "\U0001F410"),
    (("hare", "rabbit"), "\U0001F430"),
    (("sloth",), "\U0001F9A5"),
    (("salamander", "lizard"), "\U0001F98E"),
    (("koi", "fish"), "\U0001F41F"),
    (("raccoon",), "\U0001F99D"),
    (("mustang", "horse"), "\U0001F40E"),
    (("tasmanian devil",), "\U0001F43E"),
    (("cherry",), "\U0001F352"),
    (("grape",), "\U0001F347"),
    (("kiwi",), "\U0001F95D"),
    (("mango",), "\U0001F96D"),
    (("pineapple",), "\U0001F34D"),
    (("strawberry",), "\U0001F353"),
    (("watermelon",), "\U0001F349"),
    (("broccoli",), "\U0001F966"),
    (("carrot",), "\U0001F955"),
    (("corn",), "\U0001F33D"),
    (("cucumber",), "\U0001F952"),
    (("mushroom",), "\U0001F344"),
    (("onion",), "\U0001F9C5"),
    (("potato",), "\U0001F954"),
    (("spinach", "leaf", "leaves"), "\U0001F96C"),
    (("tomato",), "\U0001F345"),
    (("cat",), "\U0001F408"),
]

IMG_TAG_RE = re.compile(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*>', re.IGNORECASE)
SRC_RE = re.compile(r'\bsrc="([^"]+)"')
ALT_RE = re.compile(r'\balt="([^"]*)"')


def find_alt_for(target_path):
    """Search all html files for an <img> whose src resolves to target_path, return its alt text."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            if os.path.basename(target_path) not in content:
                continue
            for m in IMG_TAG_RE.finditer(content):
                tag = m.group(0)
                sm = SRC_RE.search(tag)
                if sm and sm.group(1).lstrip("/").endswith(target_path):
                    am = ALT_RE.search(tag)
                    if am:
                        return am.group(1)
    return None


def pick_emoji(label):
    low = label.lower()
    for keywords, emoji in EMOJI_MAP:
        for kw in keywords:
            if kw in low:
                return emoji
    return None


def pick_color(key):
    h = sum(ord(c) for c in key)
    return PALETTE[h % len(PALETTE)]


def make_icon(label, key, out_path):
    color = pick_color(key)
    img = Image.new("RGB", (SIZE, SIZE), (247, 248, 251))
    draw = ImageDraw.Draw(img)
    pad = 6
    draw.ellipse([pad, pad, SIZE - pad, SIZE - pad], fill=color)

    emoji = pick_emoji(label)
    if emoji:
        try:
            font = ImageFont.truetype(f"{FONT_DIR}/seguiemj.ttf", 120)
            bbox = draw.textbbox((0, 0), emoji, font=font, embedded_color=True)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((SIZE - tw) / 2 - bbox[0], (SIZE - th) / 2 - bbox[1]), emoji, font=font, embedded_color=True)
            img.save(out_path, quality=88)
            return
        except Exception:
            pass  # fall through to text-mark treatment

    # text-mark fallback: initials, bold, centered
    words = [w for w in re.split(r"\s+", label) if w]
    initials = "".join(w[0].upper() for w in words[:2]) if words else "?"
    font = ImageFont.truetype(f"{FONT_DIR}/Poppins-Bold.ttf", 92)
    bbox = draw.textbbox((0, 0), initials, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((SIZE - tw) / 2 - bbox[0], (SIZE - th) / 2 - bbox[1]), initials, font=font, fill=(255, 255, 255))
    img.save(out_path, quality=88)


def main():
    from audit_broken_content_images import main as _unused  # noqa: ensure module importable path context
    import importlib
    audit = importlib.import_module("audit_broken_content_images")

    # Re-run the broken-image scan in-process to get the current list
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        audit.main()
    output = buf.getvalue()

    targets = []
    for line in output.splitlines():
        m = re.match(r"^(assets/\S+|images/\S+)\s+\((\d+) refs\)$", line)
        if m:
            targets.append(m.group(1))

    made, skipped = [], []
    for target in targets:
        if target.endswith("/") or target == "" or target.startswith("assets/images/flags/"):
            # flags need factually-correct geography, not a generic emoji
            # badge -- handled separately (see gen_flag_egypt.py), never here.
            skipped.append(target)
            continue
        label = find_alt_for(target)
        if not label:
            label = os.path.splitext(os.path.basename(target))[0].replace("-", " ").title()
        out_path = os.path.join(ROOT, target)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        make_icon(label, target, out_path)
        made.append((target, label))

    print(f"Generated {len(made)} icon(s), skipped {len(skipped)} malformed target(s)")
    for t, l in made:
        print(f"  {t}  <-  \"{l}\"")
    for s in skipped:
        print(f"  SKIPPED: {s!r}")


if __name__ == "__main__":
    main()
