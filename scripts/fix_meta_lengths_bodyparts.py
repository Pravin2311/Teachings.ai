#!/usr/bin/env python3
"""Fixes title/description length across learn/body-parts/*.html (excluding index.html)."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

NAMES = ["Arms", "Ears", "Eyes", "Feet", "Hands", "Head", "Legs", "Mouth", "Nose", "Stomach"]
LONG_SUFFIX = {"Hands", "Mouth", "Stomach"}  # already fit with the shorter template

NEW_DESCS = {
    "arms": "Learn about your arms for kids: how you lift, hug, and throw, and fun arm facts to explore! Perfect for preschoolers and kindergarten body learning.",
    "feet": "Learn about your feet for kids: how you walk, run, and jump, and fun foot facts to explore! Perfect for preschoolers and kindergarten body learning.",
    "head": "Learn about your head for kids: what it does, what’s inside, and fun head facts to explore! Perfect for preschoolers and kindergarten body learning.",
    "legs": "Learn about your legs for kids: how you stand, run, and kick, and fun leg facts to explore! Perfect for preschoolers and kindergarten body learning.",
    "nose": "Learn about your nose for kids: how it smells, what it does, and fun nose facts to explore! Perfect for preschoolers and kindergarten body learning.",
}


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for name in NAMES:
        slug = name.lower()
        fname = f"learn/body-parts/{slug}.html"
        if name in LONG_SUFFIX:
            new_title = f"{name} for Kids: Learn About Your {name} & Fun Facts"
        else:
            new_title = f"{name} for Kids: Learn About Your {name} with Fun Facts"
        new_desc = NEW_DESCS.get(slug)

        if not (TITLE_MIN <= len(new_title) <= TITLE_MAX):
            print(f"[BAD TITLE LEN {len(new_title)}] {fname}: {new_title}")
            bad += 1
            continue
        if new_desc is not None and not (DESC_MIN <= len(new_desc) <= DESC_MAX):
            print(f"[BAD DESC LEN {len(new_desc)}] {fname}: {new_desc}")
            bad += 1
            continue
        ok += 1
        print(f"[{'DRY' if dry_run else 'OK'}] {fname} title={len(new_title)} desc={len(new_desc) if new_desc else 'unchanged'}")
        if dry_run:
            continue
        src = open(fname, encoding="utf-8").read()
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
