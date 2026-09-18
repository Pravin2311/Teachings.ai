#!/usr/bin/env python3
"""Fixes title/description length across teachers/*.html. Bespoke articles,
hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "teachers/brain-break-activities.html": (
        None,
        "Quick 2-10 minute brain break activities for the classroom, sorted by purpose — energizers, calm-down resets, and focus boosters between lessons.",
    ),
    "teachers/bulletin-board-ideas.html": (
        "Bulletin Board Ideas That Actually Support Learning",
        "Practical bulletin board ideas by type — welcome boards, interactive learning boards, student work showcases, and seasonal themes for busy teachers.",
    ),
    "teachers/classroom-management-strategies.html": (
        "Classroom Management Strategies That Actually Work",
        "Proactive routines, positive reinforcement, transition management, and de-escalation techniques that reduce disruptions for preschool through elementary.",
    ),
    "teachers/icebreakers-and-morning-meetings.html": (
        "Icebreakers & Morning Meeting Ideas for the Classroom",
        "A real morning meeting structure, icebreaker activities sorted by time available, and practical tips for shy or reluctant participants in class.",
    ),
    "teachers/index.html": (
        "Teacher Resource Center: Classroom Strategies & Activities",
        "Practical classroom resources for teachers — management strategies, icebreakers, morning meeting ideas, and more, grounded in what actually works.",
    ),
    "teachers/lesson-plan-basics.html": (
        "Lesson Plan Basics: A Simple, Reusable Structure Too",
        "A simple, reusable lesson plan structure using the gradual release model (I do, we do, you do), with time-blocking and differentiation tips.",
    ),
    "teachers/seasonal-classroom-activities.html": (
        "Seasonal Classroom Activities That Still Teach Well",
        "Season-based classroom activities for fall, winter, spring, and summer that tie into science, writing, and math, organized by nature and weather.",
    ),
    "teachers/stem-classroom-projects.html": (
        "STEM Classroom Projects: Simple, Hands-On Ideas Too",
        "Simple, low-equipment STEM classroom projects across science, technology, engineering, and math, sorted by grade band and time needed for class.",
    ),
    "teachers/using-flashcards-effectively.html": (
        None,
        "How to use flashcards for real learning gains — spaced repetition, active recall, and group games that outperform passive review for sight words.",
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
