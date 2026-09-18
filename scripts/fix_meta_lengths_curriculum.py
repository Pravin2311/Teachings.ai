#!/usr/bin/env python3
"""Fixes title/description length across curriculum/*.html. Bespoke articles,
hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "curriculum/deschooling-transitioning-from-traditional-school.html": (
        "Deschooling: Transitioning from Traditional School",
        "What deschooling is, how long it typically takes, and why a decompression period before formal curriculum helps both kids and parents reset.",
    ),
    "curriculum/homeschool-budget-what-it-actually-costs.html": (
        None,
        "A realistic breakdown of homeschool costs — from near-free using library and public resources to a full boxed curriculum — and where money goes.",
    ),
    "curriculum/homeschool-co-ops-and-support-groups.html": (
        "Homeschool Co-ops and Support Groups: Finding Your Community",
        "What a homeschool co-op actually is, how it differs from a support group, and practical ways to find or start one to ease homeschool isolation.",
    ),
    "curriculum/homeschool-daily-weekly-schedule.html": (
        "How to Build a Homeschool Daily and Weekly Schedule",
        "Block scheduling vs. time-based scheduling, sample daily structures by age, loop scheduling for subjects, and how to build in flexibility too.",
    ),
    "curriculum/homeschool-record-keeping-and-portfolios.html": (
        "Homeschool Record-Keeping and Portfolio Basics Guide",
        "Practical homeschool record-keeping — what to track, simple portfolio systems compared, and how to build a running record without a daily chore.",
    ),
    "curriculum/homeschool-scope-and-sequence-by-grade.html": (
        None,
        "A practical homeschool scope and sequence by grade band, covering reading, math, science, and social studies benchmarks to use flexibly today.",
    ),
    "curriculum/homeschool-socialization-what-research-says.html": (
        "Homeschool Socialization: What the Research Actually Says",
        "What research actually shows about homeschooled children's social development, and practical ways to build real peer connection every single day.",
    ),
    "curriculum/homeschooling-multiple-ages-at-once.html": (
        None,
        "How to homeschool multiple children at different ages without separate full curricula — combining subjects, independent work, and a schedule.",
    ),
    "curriculum/how-to-choose-a-homeschool-curriculum.html": (
        None,
        "A practical guide to choosing a homeschool curriculum — the major teaching approaches compared, key questions to ask, and how to trial first.",
    ),
    "curriculum/index.html": (
        "Homeschool Curriculum Hub: Choosing & Planning Your Approach",
        "Practical homeschool curriculum guidance — how to choose an approach, compare teaching philosophies, and plan what to cover by grade level too.",
    ),
    "curriculum/teaching-math-when-youre-not-a-math-person.html": (
        None,
        "Practical strategies for homeschooling parents who dread math — separating rusty memory from teaching ability, and staying one lesson ahead.",
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
