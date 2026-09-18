#!/usr/bin/env python3
"""Fixes title/description length across learn/fruits/*.html (excluding index.html)."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

NEW_TITLES = {
    "apple": "Apple for Kids – Facts, Benefits & Fun Activities Too",
    "banana": "Banana for Kids – Facts, Benefits & How They Grow Up",
    "cherry": "Cherry for Kids: Sweet, Tart & Fun Facts to Explore",
    "kiwi": "Kiwi Fruit for Kids: Fuzzy Outside, Green Inside & Facts",
}

NEW_DESCS = {
    "apple": "Learn all about Apples for kids! Discover red and green apples, health benefits, and how they grow on trees. Great for kindergarten nutrition.",
    "banana": "Learn all about Bananas for kids! Discover why they are yellow, how they grow in bunches, and health benefits like potassium for young kids.",
    "cherry": "Learn all about Cherries for kids! Discover sweet and tart varieties, how they grow in pairs on trees, and fun facts about this tiny fruit today.",
    "grapes": "Learn all about Grapes for kids! Discover red, green, and purple grapes, how they grow on vines, and fun facts about raisins for young kids.",
    "kiwi": "Learn all about Kiwi Fruit for kids! Discover the fuzzy skin, bright green flesh, tiny seeds, and how they grow on vines. Fun for young kids.",
    "mango": "Learn all about Mangoes for kids! Discover why it's the King of Fruits, how it grows in the tropics, and fun juicy facts for young learners.",
    "orange": "Learn all about Oranges for kids! Discover juicy segments, Vitamin C benefits, how they grow on trees, and fun facts for young curious learners.",
    "pineapple": "Learn all about Pineapples for kids! Discover how they grow on plants, health benefits, and why they're named after pine cones and fun facts.",
    "strawberry": "Learn all about Strawberries for kids! Discover why the seeds are on the outside, health benefits, and how they grow on plants for young kids.",
    "watermelon": "Learn all about Watermelons for kids! Discover why they are so juicy, how they grow on vines, and fun facts about seedless varieties too today.",
}

ALL_SLUGS = ["apple", "banana", "cherry", "grapes", "kiwi", "mango", "orange", "pineapple", "strawberry", "watermelon"]


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for slug in ALL_SLUGS:
        fname = f"learn/fruits/{slug}.html"
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
