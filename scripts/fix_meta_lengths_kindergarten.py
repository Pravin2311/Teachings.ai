#!/usr/bin/env python3
"""Fixes title/description length across kindergarten/*.html. Bespoke
articles, hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "kindergarten/first-day-of-kindergarten-guide.html": (
        None,
        "Practical preparation for the first day of kindergarten — what to practice beforehand, handling separation anxiety, and what matters most that day.",
    ),
    "kindergarten/index.html": (
        "Kindergarten Learning: Skills, Milestones & Guides",
        None,
    ),
    "kindergarten/kindergarten-handwriting-and-pencil-grip.html": (
        None,
        "The mechanics of kindergarten handwriting instruction — pencil grip types, letter formation strokes, and simple ways to build hand strength.",
    ),
    "kindergarten/kindergarten-math-skills.html": (
        "Kindergarten Math Skills: What to Expect & Practice",
        None,
    ),
    "kindergarten/kindergarten-phonemic-awareness.html": (
        "Kindergarten Phonemic Awareness: Hearing Sounds in Words",
        "What phonemic awareness is, how it differs from sight word memorization, and simple oral activities that build the sound skills kids need to read.",
    ),
    "kindergarten/kindergarten-science-exploration.html": (
        "Kindergarten Science: Observation & Curriculum Basics",
        "What kindergarten science actually covers — observation skills, living vs. nonliving, and simple weather patterns — for hands-on science activities.",
    ),
    "kindergarten/kindergarten-social-emotional-skills.html": (
        "Kindergarten Social-Emotional Skills for the Classroom",
        "The classroom-specific social skills kindergartners are learning — turn-taking, following group directions, and self-regulation — and how to help.",
    ),
    "kindergarten/kindergarten-writing-skills.html": (
        "Kindergarten Writing: From Scribbles to Sentences Too",
        "The typical kindergarten writing progression — from scribbles and letter-like forms to invented spelling and simple sentences — stage by stage.",
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
