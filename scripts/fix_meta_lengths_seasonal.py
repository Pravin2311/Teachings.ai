#!/usr/bin/env python3
"""Fixes title/description length across seasonal/*.html. Bespoke articles,
hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "seasonal/back-to-school-transition-activities.html": (
        None,
        "Practical activities for the specific weeks before school starts — resetting sleep schedules, rebuilding routine, and easing first-week jitters.",
    ),
    "seasonal/fall-learning-activities-for-families.html": (
        None,
        "A full season of fall learning activities for families — nature observation, reading, math, and art projects tied to autumn, week by week too.",
    ),
    "seasonal/index.html": (
        "Seasonal Content Calendar: Learning Activities by Season",
        None,
    ),
    "seasonal/rainy-day-and-snow-day-activity-plans.html": (
        None,
        "A cross-seasonal contingency plan for unexpected indoor days — quick-setup activities and a simple decision tree for any time of year at all.",
    ),
    "seasonal/seasonal-read-aloud-book-lists.html": (
        "Seasonal Read-Aloud Book Lists for Every Time of Year",
        "Curated read-aloud book picks organized by season, a standalone booklist resource distinct from activities inside each seasonal learning guide.",
    ),
    "seasonal/summer-learning-activities-for-families.html": (
        None,
        "A full season of summer learning activities for families — water science, outdoor math, reading challenges, and preventing summer learning loss.",
    ),
    "seasonal/winter-break-and-holiday-learning-activities.html": (
        None,
        "Keeping skills warm during the winter holiday break — baking math, holiday-themed crafts, and family traditions for the whole family to enjoy.",
    ),
    "seasonal/winter-learning-activities-for-families.html": (
        None,
        "A full season of winter learning activities for families — indoor science, math with snow and temperature, reading, and sensory play at home.",
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
