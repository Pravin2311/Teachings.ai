#!/usr/bin/env python3
"""Fixes title/description length across interactive/*.html. Bespoke pages,
hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "interactive/index.html": (
        "Interactive Learning: Printable Trackers & Certificates",
        None,
    ),
    "interactive/printable-behavior-reward-chart.html": (
        None,
        "A free printable weekly behavior reward chart — print it directly from your browser, no download needed, with guidance on picking target behaviors.",
    ),
    "interactive/printable-certificate-of-achievement.html": (
        None,
        "A free printable certificate of achievement for kids — print it directly from your browser, no download needed, with tips on meaningful recognition.",
    ),
    "interactive/printable-goal-tracker.html": (
        "Printable Goal Tracker for Kids: Free & Simple to Use",
        "A free printable goal tracker for kids — print it directly from your browser, no download needed. Breaks one goal into small, trackable steps.",
    ),
    "interactive/printable-multiplication-chart.html": (
        None,
        "A free printable 1-12 multiplication reference chart — print it directly from your browser, no download needed. A quick reference, not a worksheet.",
    ),
    "interactive/printable-reading-log.html": (
        "Printable Reading Log for Kids: Free & Easy to Use",
        "A free printable reading log for kids — print it directly from your browser, no download needed, with guidance on why tracking builds motivation.",
    ),
    "interactive/printable-weekly-planner-for-kids.html": (
        "Printable Weekly Planner for Kids: Free Daily Layout",
        "A free printable weekly planner for kids — print it directly from your browser, no download needed. A simple daily task layout for the week.",
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
