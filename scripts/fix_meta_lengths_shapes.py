#!/usr/bin/env python3
"""Fixes title/description length across learn/shapes/*.html (excluding index.html).
Every page shares an identical template, differing only by the shape name, so one
new template (verified to fit [50,60]/[140,155] for every name in the cluster)
is applied uniformly.
"""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

NAMES = ["Circle", "Crescent", "Diamond", "Heart", "Hexagon", "Octagon", "Oval",
         "Pentagon", "Rectangle", "Square", "Star", "Triangle"]


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for name in NAMES:
        fname = f"learn/shapes/{name.lower()}.html"
        new_title = f"The {name} Shape for Kids: Sides, Angles & Fun Facts"
        new_desc = (
            f"Learn all about the {name} shape! Discover how many sides it has, "
            f"real-world examples to spot, and fun facts for preschool and kindergarten kids."
        )
        if not (TITLE_MIN <= len(new_title) <= TITLE_MAX) or not (DESC_MIN <= len(new_desc) <= DESC_MAX):
            print(f"[BAD LEN] {fname} title={len(new_title)} desc={len(new_desc)}")
            bad += 1
            continue
        ok += 1
        print(f"[{'DRY' if dry_run else 'OK'}] {fname}")
        print(f"    title({len(new_title)}): {new_title}")
        print(f"    desc ({len(new_desc)}): {new_desc}")
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
