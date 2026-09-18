#!/usr/bin/env python3
"""Fixes title/description length across learn/phonics/*.html (excluding index.html)."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

PAIRS = [
    ("ball", "B", "Ball"), ("egg", "E", "Egg"), ("fish", "F", "Fish"),
    ("goat", "G", "Goat"), ("hat", "H", "Hat"), ("ice", "I", "Ice"),
    ("jug", "J", "Jug"), ("kite", "K", "Kite"), ("mug", "M", "Mug"),
    ("notebook", "N", "Notebook"), ("octopus", "O", "Octopus"), ("pen", "P", "Pen"),
    ("queen", "Q", "Queen"), ("rat", "R", "Rat"), ("sun", "S", "Sun"),
    ("tap", "T", "Tap"), ("umbrella", "U", "Umbrella"), ("van", "V", "Van"),
    ("wolf", "W", "Wolf"), ("xylophone", "X", "Xylophone"), ("yak", "Y", "Yak"),
]


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for slug, letter, word in PAIRS:
        fname = f"learn/phonics/{slug}.html"
        new_title = f"{letter} is for {word} – Fun Phonics for Kids | Teachings.ai"
        new_desc = (
            f"Learn the letter {letter} sound with {word}! Fun phonics facts, pronunciation "
            f"practice tips, and a matching quiz for preschool and kindergarten early readers."
        )
        if not (TITLE_MIN <= len(new_title) <= TITLE_MAX) or not (DESC_MIN <= len(new_desc) <= DESC_MAX):
            print(f"[BAD LEN] {fname} title={len(new_title)} desc={len(new_desc)}")
            bad += 1
            continue
        ok += 1
        print(f"[{'DRY' if dry_run else 'OK'}] {fname} title={len(new_title)} desc={len(new_desc)}")
        if dry_run:
            continue
        src = open(fname, encoding="utf-8").read()
        tm = TITLE_RE.search(src)
        src = src[: tm.start(1)] + new_title.replace("&", "&amp;") + src[tm.end(1):]
        dm = DESC_RE.search(src)
        src = src[: dm.start(3)] + new_desc.replace("&", "&amp;") + src[dm.end(3):]
        with open(fname, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
    print(f"\nok={ok} bad={bad} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
