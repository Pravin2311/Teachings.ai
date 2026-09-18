#!/usr/bin/env python3
"""Fixes title/description length for the 'flag template' learn/country/*.html
pages (Germany, Italy, Mexico, Portugal, Russia, Switzerland) -- countries whose
page only has a short generic blurb, not the richer highlight-list template."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

NAMES = ["Germany", "Italy", "Mexico", "Portugal", "Russia", "Switzerland"]


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for name in NAMES:
        fname = f"learn/country/{name.lower()}.html"
        if name == "Italy":
            new_title = "Italy for Kids – Flag, Facts & Fun Geography Guide"
        else:
            new_title = f"{name} for Kids: Flag, Facts & Fun Geography Guide"
        new_desc = (
            f"Learn all about {name}! Discover its flag, fun facts, and where it is in "
            f"the world, in a page made just for preschool and kindergarten geography."
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
