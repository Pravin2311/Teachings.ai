#!/usr/bin/env python3
"""Fixes title/description length across lesson-plans/*.html. Bespoke
articles, hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "lesson-plans/character-traits-lesson-plan.html": (
        "Character Traits Lesson Plan for Elementary Teachers",
        "A ready-to-use lesson plan teaching character traits and how to identify them from a character's actions and words, with assessment ideas included.",
    ),
    "lesson-plans/community-helpers-lesson-plan.html": (
        "Community Helpers Lesson Plan for Early Elementary",
        None,
    ),
    "lesson-plans/index.html": (
        "Free Lesson Plans: Ready-to-Use Classroom Lessons Too",
        "Free, ready-to-use lesson plans with objectives, materials, a gradual-release procedure, and assessment ideas across science, math, and language arts.",
    ),
    "lesson-plans/introduction-to-fractions-lesson-plan.html": (
        None,
        "A ready-to-use lesson plan introducing fractions with hands-on food-based activities and a gradual-release procedure, free to use and adapt for class.",
    ),
    "lesson-plans/main-idea-and-supporting-details-lesson-plan.html": (
        None,
        "A ready-to-use lesson plan teaching main idea and supporting details using a hamburger graphic organizer, with assessment ideas for teachers.",
    ),
    "lesson-plans/map-skills-lesson-plan.html": (
        "Map Skills Lesson Plan for Elementary Classrooms Too",
        "A ready-to-use lesson plan teaching basic map skills — cardinal directions, map keys, and simple map reading — with a hands-on classroom activity.",
    ),
    "lesson-plans/parts-of-a-plant-lesson-plan.html": (
        "Parts of a Plant Lesson Plan for Elementary Science",
        "A ready-to-use lesson plan teaching the parts of a plant and their functions, with a hands-on diagram activity and assessment ideas for teachers.",
    ),
    "lesson-plans/telling-time-lesson-plan.html": (
        "Telling Time Lesson Plan for Elementary Classrooms",
        "A ready-to-use lesson plan teaching how to tell time to the hour and half hour using a paper clock, with a gradual-release procedure for teachers.",
    ),
    "lesson-plans/water-cycle-lesson-plan.html": (
        None,
        "A ready-to-use elementary water cycle lesson plan with objectives, materials, and a gradual-release procedure, free to use and adapt for class.",
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
