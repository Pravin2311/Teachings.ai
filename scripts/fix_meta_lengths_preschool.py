#!/usr/bin/env python3
"""Fixes title/description length across preschool/*.html. Bespoke articles,
hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "preschool/building-language-through-play.html": (
        None,
        "How everyday play naturally builds vocabulary and language skills in preschoolers — narrating play, open-ended questions, and why quantity matters.",
    ),
    "preschool/circle-time-activities.html": (
        None,
        "A simple, repeatable circle time structure for preschool — opening song, calendar, and a themed activity — for a classroom or a child at home.",
    ),
    "preschool/fine-motor-activities-for-preschoolers.html": (
        None,
        "Low-prep fine motor activities for preschoolers — tweezer transfers, playdough, lacing, and more — that build hand strength for later handwriting.",
    ),
    "preschool/gross-motor-activities-for-preschoolers.html": (
        None,
        "Large-muscle movement activities for preschoolers — balance, coordination, and core strength games — that support later fine motor and focus.",
    ),
    "preschool/index.html": (
        "Preschool Activities: Fine Motor, Sensory & Readiness",
        "Preschool activity guides organized by developmental domain — fine motor, sensory play, circle time, and kindergarten readiness for home or class.",
    ),
    "preschool/managing-big-emotions-toolkit.html": (
        "Managing Big Emotions: A Preschooler's Toolkit Too",
        "Practical strategies for helping preschoolers manage big emotions — naming feelings, calm-down tools, and why tantrums are a normal part of growth.",
    ),
    "preschool/preschool-readiness-checklist.html": (
        "Preschool Readiness Checklist Before Kindergarten Too",
        "A practical, low-pressure checklist of skills that typically develop before kindergarten — academic, social, self-care, and fine motor skills.",
    ),
    "preschool/sensory-play-ideas.html": (
        None,
        "Low-cost sensory play ideas for preschoolers — sensory bins, texture exploration, and calming activities — with guidance on what sensory play builds.",
    ),
    "preschool/simple-cooking-activities-for-preschoolers.html": (
        None,
        "Safe, simple cooking tasks preschoolers can genuinely help with, and the math, science, and fine motor skills each one quietly builds every time.",
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
