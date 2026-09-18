#!/usr/bin/env python3
"""Fixes title/description length across learn/colors/*.html (excluding index.html)."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

NEW_TITLES = {
    "blue": "Blue for Kids – Ocean, Sky, Animals & Fun Facts to Learn",
    "red": "Red for Kids – Objects, Facts & Fun Learning Activities",
    "yellow": "Yellow for Kids – Sun, Stars, Bananas & Fun Facts Too",
}

NEW_DESCS = {
    "black": "Learn all about the color Black! Discover the night sky, space, black animals like panthers, and the science of light absorption for young learners.",
    "blue": "Learn all about the color Blue! Discover blue animals like whales, blue fruits like blueberries, and the science of why the sky looks so blue.",
    "brown": "Learn all about the color Brown! Discover earth, trees, chocolate, brown animals like bears and owls, and the fun science of mixing colors together.",
    "green": "Learn all about the color Green! Discover green plants, animals like frogs, the science of chlorophyll, and fun mixing activities for young kids.",
    "orange": "Learn all about the color Orange! Discover orange fruits like oranges and pumpkins, autumn leaves, and the science of mixing red and yellow.",
    "pink": "Learn all about the color Pink! Discover pink animals like flamingos, sweet fruits, beautiful flowers, and the science of mixing red and white.",
    "purple": "Learn all about the color Purple! Discover royal history, purple flowers like lavender, fruits like grapes, and the science of mixing colors.",
    "white": "Learn all about the color White! Discover snow, clouds, white animals like polar bears, and the fun science of light reflection for young kids.",
    "yellow": "Learn all about the color Yellow! Discover the sun, stars, yellow fruits like bananas and lemons, and the science of light for young learners.",
}

ALL_SLUGS = ["black", "blue", "brown", "green", "orange", "pink", "purple", "red", "white", "yellow"]


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for slug in ALL_SLUGS:
        fname = f"learn/colors/{slug}.html"
        new_title = NEW_TITLES.get(slug)
        new_desc = NEW_DESCS.get(slug)
        if new_title is not None and not (TITLE_MIN <= len(new_title) <= TITLE_MAX):
            print(f"[BAD TITLE LEN {len(new_title)}] {fname}: {new_title}")
            bad += 1
            continue
        if new_desc is not None and not (DESC_MIN <= len(new_desc) <= DESC_MAX):
            print(f"[BAD DESC LEN {len(new_desc)}] {fname}: {new_desc}")
            bad += 1
            continue
        ok += 1
        print(f"[{'DRY' if dry_run else 'OK'}] {fname} title={len(new_title) if new_title else 'unchanged'} desc={len(new_desc) if new_desc else 'unchanged'}")
        if dry_run:
            continue
        src = open(fname, encoding="utf-8").read()
        if new_title is not None:
            tm = TITLE_RE.search(src)
            src = src[: tm.start(1)] + new_title.replace("&", "&amp;") + src[tm.end(1):]
        if new_desc is not None:
            dm = DESC_RE.search(src)
            src = src[: dm.start(3)] + new_desc.replace("&", "&amp;") + src[dm.end(3):]
        with open(fname, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
    print(f"\nok={ok} bad={bad} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
