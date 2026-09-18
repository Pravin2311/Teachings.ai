#!/usr/bin/env python3
"""Fixes description length across learn/numbers/*.html (excluding index.html).
Titles are already in range; only the (too-short) description needs a change."""
import re
import sys

DESC_MIN, DESC_MAX = 140, 155

DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

NUMS = [
    ("0", "Zero"), ("1", "One"), ("2", "Two"), ("3", "Three"), ("4", "Four"),
    ("5", "Five"), ("6", "Six"), ("7", "Seven"), ("8", "Eight"), ("9", "Nine"), ("10", "Ten"),
]


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for n, w in NUMS:
        fname = f"learn/numbers/number-{n}.html"
        new_desc = (
            f"Learn all about the number {n} ({w})! Fun facts, real-life counting examples, "
            f"and a printable quiz for preschool and kindergarten kids to enjoy."
        )
        if not (DESC_MIN <= len(new_desc) <= DESC_MAX):
            print(f"[BAD DESC LEN {len(new_desc)}] {fname}: {new_desc}")
            bad += 1
            continue
        ok += 1
        print(f"[{'DRY' if dry_run else 'OK'}] {fname} desc={len(new_desc)}")
        if dry_run:
            continue
        src = open(fname, encoding="utf-8").read()
        dm = DESC_RE.search(src)
        src = src[: dm.start(3)] + new_desc.replace("&", "&amp;") + src[dm.end(3):]
        with open(fname, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
    print(f"\nok={ok} bad={bad} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
