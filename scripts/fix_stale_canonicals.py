#!/usr/bin/env python3
"""Fixes canonical <link> tags that point to a URL other than the page's own
current path. Most of these are leftovers from a directory rename
(learn/animals/birds/* -> learn/birds/*, learn/bodyparts/* ->
learn/body-parts/*) where the file moved but the canonical wasn't updated,
plus a handful of one-off copy/paste errors. Each canonical is rewritten to
point to the page's own real, current URL.
"""
import re
import sys

CANONICAL_RE = re.compile(r'(<link\s+[^>]*rel=["\']canonical["\'][^>]*href=)(["\'])(.*?)\2', re.S | re.I)

# file -> correct canonical URL (self)
FIXES = {}

for name in ["duck", "eagle", "flamingo", "hen", "hummingbird", "owl", "parrot", "peacock", "pigeon", "sparrow"]:
    FIXES[f"learn/birds/{name}.html"] = f"https://www.teachings.ai/learn/birds/{name}.html"

for name in ["arms", "ears", "eyes", "feet", "hands", "head", "index", "legs", "mouth", "nose", "stomach"]:
    FIXES[f"learn/body-parts/{name}.html"] = f"https://www.teachings.ai/learn/body-parts/{name}.html"

FIXES["learn/alphabets/letter-d.html"] = "https://www.teachings.ai/learn/alphabets/letter-d.html"
FIXES["learn/fruits/grapes.html"] = "https://www.teachings.ai/learn/fruits/grapes.html"
FIXES["learn/vehicles/ships.html"] = "https://www.teachings.ai/learn/vehicles/ships.html"
FIXES["phonic-words.html"] = "https://www.teachings.ai/phonic-words.html"
FIXES["privacy-policy.html"] = "https://www.teachings.ai/privacy-policy.html"


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for fname, correct_url in FIXES.items():
        src = open(fname, encoding="utf-8").read()
        m = CANONICAL_RE.search(src)
        if not m:
            print(f"[NO CANONICAL FOUND] {fname}")
            bad += 1
            continue
        old_url = m.group(3)
        if old_url == correct_url:
            continue
        print(f"[{'DRY' if dry_run else 'OK'}] {fname}: {old_url} -> {correct_url}")
        ok += 1
        if dry_run:
            continue
        new_src = src[: m.start(3)] + correct_url + src[m.end(3):]
        with open(fname, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_src)
    print(f"\nfixed={ok} problems={bad} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
