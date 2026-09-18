#!/usr/bin/env python3
"""Fixes title/description length across learn/nature/*.html (excluding index.html).
Extracts Name + clause from the existing near-uniform template, then generates
several candidate phrasings per page and picks the best in-range one.
"""
import re
import sys
import html as htmlmod

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)
TITLE_NAME_RE = re.compile(r"^(.+?) for Kids")
DESC_PAT = re.compile(
    r"^Learn all about an? (?P<name>.+?)!\s*Discover fun facts about (?P<clause>.+?)\.\s*"
    r"Perfect for preschool and kindergarten nature exploration\.$"
)

FILES = [
    "learn/nature/anthill.html", "learn/nature/aurora.html", "learn/nature/beach.html",
    "learn/nature/camp.html", "learn/nature/cave.html", "learn/nature/desert.html",
    "learn/nature/eaglenest.html", "learn/nature/forest.html", "learn/nature/lake.html",
    "learn/nature/mountain.html", "learn/nature/ocean.html", "learn/nature/river.html",
    "learn/nature/sunset.html", "learn/nature/volcano.html", "learn/nature/waterfall.html",
]


def pick(candidates, lo, hi):
    in_range = [c for c in candidates if lo <= len(c) <= hi]
    if in_range:
        mid = (lo + hi) / 2
        return min(in_range, key=lambda c: abs(len(c) - mid))
    return None


def build_title(name):
    prefixes = ["", "The ", "Explore the "]
    joins = [" for Kids: ", " for Kids – "]
    suffixes = [
        "Fun Facts & Nature Learning",
        "Fun Facts & Nature Guide",
        "Cool Facts & Nature Learning",
        "Amazing Facts & Nature Learning",
        "Facts & Nature Learning",
        "Fun Facts for Curious Kids",
    ]
    candidates = [f"{p}{name}{j}{s}" for p in prefixes for j in joins for s in suffixes]
    return pick(candidates, TITLE_MIN, TITLE_MAX) or min(candidates, key=lambda c: abs(len(c) - 55))


def build_desc(name, clause):
    openings = [f"Learn about a {name}!", f"Learn all about a {name}!", f"Discover a {name}!"]
    bodies = [f"Discover fun facts about {clause}.", f"Here are fun facts about {clause}.", f"Fun facts: {clause}."]
    tails = [
        "Great for preschool and kindergarten nature lovers.",
        "Fun for preschool and kindergarten nature explorers.",
        "Great for young nature explorers.",
        "A fun pick for preschool and kindergarten nature study.",
        "Perfect for preschool and kindergarten nature exploration.",
    ]
    candidates = [f"{o} {b} {t}" for o in openings for b in bodies for t in tails]
    return pick(candidates, DESC_MIN, DESC_MAX) or min(candidates, key=lambda c: abs(len(c) - 147))


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for fname in FILES:
        src = open(fname, encoding="utf-8").read()
        tm = TITLE_RE.search(src)
        dm = DESC_RE.search(src)
        old_title = htmlmod.unescape(tm.group(1).strip())
        old_desc = htmlmod.unescape(dm.group(3).strip())

        nm = TITLE_NAME_RE.match(old_title)
        name = nm.group(1).strip() if nm else None
        dm2 = DESC_PAT.match(old_desc)

        if not name or not dm2:
            print(f"[NO-MATCH] {fname}")
            print(f"    title: {old_title}")
            print(f"    desc:  {old_desc}")
            bad += 1
            continue

        clause = dm2.group("clause")
        new_title = build_title(name)
        new_desc = build_desc(name, clause)

        ok_t = TITLE_MIN <= len(new_title) <= TITLE_MAX
        ok_d = DESC_MIN <= len(new_desc) <= DESC_MAX
        status = "ok" if (ok_t and ok_d) else "out-of-range"
        if status != "ok":
            bad += 1
        else:
            ok += 1
        print(f"[{'DRY' if dry_run else status.upper()}] {fname}")
        print(f"    title({len(new_title)}): {new_title}")
        print(f"    desc ({len(new_desc)}): {new_desc}")

        if dry_run or status != "ok":
            continue

        src = src[: tm.start(1)] + new_title.replace("&", "&amp;") + src[tm.end(1):]
        dm3 = DESC_RE.search(src)
        src = src[: dm3.start(3)] + new_desc.replace("&", "&amp;") + src[dm3.end(3):]
        with open(fname, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)

    print(f"\nok={ok} bad={bad} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
