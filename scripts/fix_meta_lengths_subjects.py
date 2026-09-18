#!/usr/bin/env python3
"""Fixes title/description length across subjects/*.html. Bespoke hub pages,
hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "subjects/index.html": (
        "Subject Hubs: Every Resource, Organized by Skill Too",
        "Complete subject-by-subject maps of Teachings.ai's resources — games, worksheets, curriculum guidance, and parent strategies by skill progression.",
    ),
    "subjects/language-arts-hub.html": (
        "Language Arts Hub: Reading, Phonics & Writing Resources",
        "A complete map of Teachings.ai's language arts resources — phonics games, reading guides, grammar practice, and book lists by skill level today.",
    ),
    "subjects/math-hub.html": (
        None,
        "A complete map of Teachings.ai's math resources — games, worksheets, curriculum guidance, and parent strategies organized by skill and grade.",
    ),
    "subjects/science-hub.html": (
        "Science Hub: Every Resource, Organized by Topic Too",
        "A complete map of Teachings.ai's science resources — living things, earth and space, and technology, organized by topic with games and guidance.",
    ),
    "subjects/social-studies-hub.html": (
        "Social Studies Hub: Geography, Community & Civics Too",
        "A complete map of Teachings.ai's social studies resources — world geography, countries and flags, and community and civics for all families.",
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
