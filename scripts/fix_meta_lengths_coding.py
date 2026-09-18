#!/usr/bin/env python3
"""Fixes title/description length across coding/*.html. Bespoke articles,
hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "coding/best-beginner-coding-apps.html": (
        "Best Beginner Coding Apps and Websites for Kids Too",
        "A curated list of well-known, kid-friendly coding platforms by age band — from drag-and-drop block coding to guided lessons — what to look for.",
    ),
    "coding/coding-games-and-puzzles-for-beginners.html": (
        None,
        "Puzzle-based activities that build the logical thinking behind coding — maze pathfinding, sequencing puzzles, and pattern logic — with real examples.",
    ),
    "coding/coding-vocabulary-for-kids.html": (
        "Coding Vocabulary for Kids: Key Terms Explained Well",
        None,
    ),
    "coding/how-coding-connects-to-math.html": (
        "How Coding Skills Connect to Math: A Parent's Guide",
        "The genuine overlap between coding and math skills — coordinates, sequencing, logical reasoning, and estimation — and how coding reinforces math.",
    ),
    "coding/index.html": (
        "Coding for Kids: Unplugged Activities & Guides Too",
        "A beginner-friendly introduction to coding for kids — what coding is, unplugged activities, key vocabulary, and a list of kid-friendly platforms.",
    ),
    "coding/simple-algorithms-kids-can-write.html": (
        "Simple Algorithms Kids Can Write Before Any Screen",
        None,
    ),
    "coding/unplugged-coding-activities.html": (
        None,
        None,
    ),
    "coding/what-is-coding-for-kids.html": (
        None,
        "A simple, honest explanation of what coding actually is, using everyday analogies kids already understand — recipes and step-by-step directions.",
    ),
    "coding/why-mistakes-help-you-learn-to-code.html": (
        None,
        "Why coding errors are a normal, useful part of the process rather than a sign of failure — reframing debugging as detective work for young coders.",
    ),
}


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad, skip = 0, 0, 0
    for fname, (new_title, new_desc) in CHANGES.items():
        if new_title is None and new_desc is None:
            skip += 1
            continue
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
    print(f"\nok={ok} bad={bad} skip={skip} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
