#!/usr/bin/env python3
"""Fixes title/description length across ages/*.html. Titles trim the " | Teachings.ai"
suffix and shorten a "Milestones" clause; descriptions trim to fit."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "ages/age-2.html": (
        "2-Year-Old Learning Hub: Toddler Milestones & Free Resources",
        "What's typical for a 2-year-old across talking, sensory play, and early independence, plus screen-time guidance and simple everyday activities.",
    ),
    "ages/age-3.html": (
        "3-Year-Old Learning Hub: Toddler Milestones & Free Resources",
        "What's typical for a 3-year-old across pre-reading, early counting, and sensory exploration, plus curated free games, worksheets, and a daily rhythm.",
    ),
    "ages/age-4.html": (
        "4-Year-Old Learning Hub: Milestones & Free Resources",
        None,
    ),
    "ages/age-5.html": (
        "5-Year-Old Learning Hub: Kindergarten Milestones Too",
        None,
    ),
    "ages/age-6.html": (
        "6-Year-Old Learning Hub: First Grade Milestones Too",
        "What's typical for a 6-year-old in first grade across reading fluency, addition and subtraction, and science, plus curated free games and worksheets.",
    ),
    "ages/age-7.html": (
        "7-Year-Old Learning Hub: Second Grade Milestones Too",
        "What's typical for a 7-year-old in second grade across reading fluency, early multiplication, and science, plus curated free games and worksheets.",
    ),
    "ages/age-8.html": (
        "8-Year-Old Learning Hub: Milestones & Free Resources",
        "What's typical for an 8-year-old across reading comprehension, multiplication, science, and independence, plus curated free games and worksheets.",
    ),
    "ages/age-9.html": (
        "9-Year-Old Learning Hub: Fourth Grade Milestones Too",
        "What's typical for a 9-year-old across reading to learn, multiplication fluency, early fractions, and growing independence, plus free resources.",
    ),
    "ages/age-10.html": (
        "10-Year-Old Learning Hub: Fifth Grade Milestones Too",
        "What's typical for a 10-year-old across complex reading, decimals and fractions, and growing pre-teen independence, plus curated free resources.",
    ),
    "ages/age-11.html": (
        "11-Year-Old Learning Hub: Middle School Milestones Too",
        "What's typical for an 11-year-old navigating the middle school transition, ratios and pre-algebra, and growing independence, plus free resources.",
    ),
    "ages/age-12.html": (
        "12-Year-Old Learning Hub: Algebra Readiness & Free Resources",
        "What's typical for a 12-year-old approaching algebra readiness, critical reading across subjects, and growing independence, plus free resources.",
    ),
    "ages/index.html": (
        "Learning by Age: Activities & Milestones from 2 to 12",
        "Age-specific learning hubs for ages 2 through 12 — what's developmentally typical, curated activities across reading, math, and science for each age.",
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
