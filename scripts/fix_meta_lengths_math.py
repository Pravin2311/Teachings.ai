#!/usr/bin/env python3
"""Fixes title/description length across math/*.html. Bespoke articles,
hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "math/games-for-fact-fluency.html": (
        None,
        "Simple games that build addition, subtraction, and multiplication fact fluency through repetition and play, without relying on timed drills alone.",
    ),
    "math/index.html": (
        "Math Activities: Hands-On Learning Beyond Worksheets",
        "Hands-on math activities, games, and everyday strategies for building number sense, fact fluency, and fraction understanding beyond worksheets.",
    ),
    "math/math-journaling-for-kids.html": (
        None,
        "How math journaling — writing or drawing about a problem's reasoning, not just the answer — builds deeper understanding a worksheet alone can't show.",
    ),
    "math/math-talk-everyday-conversations.html": (
        "Math Talk: Everyday Conversations for Number Sense",
        "How to weave math language into everyday conversation — at meals, in the car, during chores — to build number sense without dedicated practice time.",
    ),
    "math/measurement-activities-for-kids.html": (
        "Measurement Activities for Kids: Length, Weight & Volume",
        None,
    ),
    "math/teaching-place-value-with-household-objects.html": (
        None,
        "Hands-on place value activities using household items instead of purchased base-ten blocks — bundling, grouping, and building genuine understanding.",
    ),
}


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for fname, (new_title, new_desc) in CHANGES.items():
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
