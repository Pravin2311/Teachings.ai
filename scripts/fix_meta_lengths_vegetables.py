#!/usr/bin/env python3
"""Fixes title/description length across learn/vegetables/*.html (excluding index.html)."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

NEW_TITLES = {
    "broccoli": "Broccoli for Kids – The Tiny Tree Super Veggie Facts",
    "corn": "Corn for Kids – The Golden Grain That Pops! Fun Facts",
    "onion": "Onion for Kids – The Veggie That Makes You Cry! Facts",
    "potato": "Potato for Kids – The Underground Super Spud & Facts",
    "spinach": "Spinach for Kids – The Superpower Leafy Green & Facts",
    "tomato": "Tomato for Kids – Fruit or Veggie? Facts & Fun Too",
}

NEW_DESCS = {
    "bell-pepper": "Learn all about Bell Peppers for kids! Discover why they come in red, yellow, and green, health benefits, how they grow, and yummy fun facts.",
    "broccoli": "Learn all about Broccoli for kids! Discover why it looks like a tree, health benefits, how it grows, and fun facts for young kids to explore.",
    "carrot": "Learn all about Carrots for kids! Discover orange carrots, health benefits, how they grow underground, and fun facts for young curious learners.",
    "corn": "Learn all about Corn for kids! Discover if it's a fruit, veggie, or grain, how it grows on tall stalks, and fun popcorn facts to explore today.",
    "cucumber": "Learn all about Cucumbers for kids! Discover if they are a fruit or vegetable, why they are cool, and how they grow on vines. Fun for young kids.",
    "mushroom": "Learn all about Mushrooms for kids! Discover why they aren't plants, how they grow from spores, and fun facts for young science learners today.",
    "onion": "Learn all about Onions for kids! Discover why they make you cry, different colors, health benefits, and how they grow in layers underground.",
    "potato": "Learn all about Potatoes for kids! Discover how they grow underground, different colors, health benefits, and fun facts like space potatoes.",
    "spinach": "Learn all about Spinach for kids! Discover why it gives you super strength, health benefits, how it grows, and fun Popeye facts too for kids.",
    "tomato": "Learn all about Tomatoes for kids! Discover if they are a fruit or vegetable, health benefits, how they grow on vines, and fun facts for kids.",
}

ALL_SLUGS = ["bell-pepper", "broccoli", "carrot", "corn", "cucumber", "mushroom", "onion", "potato", "spinach", "tomato"]


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for slug in ALL_SLUGS:
        fname = f"learn/vegetables/{slug}.html"
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
