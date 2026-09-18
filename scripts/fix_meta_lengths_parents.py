#!/usr/bin/env python3
"""Fixes title/description length across parents/*.html. Each page is a bespoke
article, so copy is hand-trimmed per file rather than templated."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "parents/adhd-friendly-learning-activities.html": (
        "ADHD-Friendly Learning Activities: A Guide for Parents",
        "General, practical strategies for helping a child with ADHD engage with learning — movement, structure, novelty, and clear feedback, with real examples.",
    ),
    "parents/autism-friendly-learning-activities.html": (
        "Autism-Friendly Learning Activities: A Parent Guide",
        None,
    ),
    "parents/building-executive-function-skills.html": (
        None,
        "Practical ways to build planning, organization, and self-control skills at home — everyday habits that support executive function at every age.",
    ),
    "parents/building-reading-comprehension.html": (
        None,
        "Why some kids read words fluently but don't understand them, the real strategies that build comprehension, and activities for each reading stage.",
    ),
    "parents/dyslexia-friendly-activities.html": (
        "Dyslexia-Friendly Activities: A Practical Guide for Parents",
        "What dyslexia actually is, common signs parents notice, multisensory teaching strategies that help, and how to protect confidence along the way.",
    ),
    "parents/helping-a-struggling-reader.html": (
        "Helping a Struggling Reader: A Calm Guide for Parents",
        None,
    ),
    "parents/homework-help-without-power-struggles.html": (
        None,
        "Practical strategies for reducing homework battles — setting up a workable routine, how much help is too much, and what to do when a child refuses.",
    ),
    "parents/how-to-teach-reading-at-home.html": (
        "How to Teach Reading at Home: A Step-by-Step Guide",
        "A complete, age-by-age guide to teaching your child to read at home — the five pillars of reading, a weekly routine, and activities for every stage.",
    ),
    "parents/index.html": (
        "Parent Learning Center – Guides for Teaching Kids at Home",
        "In-depth, practical guides for parents and homeschool families: how to teach reading, phonics, comprehension, and more, grounded in real learning.",
    ),
    "parents/learning-routine-by-age.html": (
        None,
        "Realistic daily and weekly learning routines for ages 2 through 12 — attention spans, sample schedules, and how much structured time is appropriate.",
    ),
    "parents/phonics-guide-for-parents.html": (
        "Phonics Guide for Parents: How to Teach Phonics at Home",
        None,
    ),
    "parents/screen-time-practical-guide.html": (
        None,
        "A balanced, guilt-free guide to screen time — age-based starting points, why quality matters more than the clock, and building healthy habits.",
    ),
    "parents/supporting-speech-development.html": (
        "Supporting Speech Development: A Practical Guide for Parents",
        "General speech development milestones by age, everyday activities that support talking, common concerns that are usually normal, and when to ask a pro.",
    ),
    "parents/when-to-seek-extra-support.html": (
        None,
        "General patterns worth noticing and discussing with a professional — this guide points toward evaluation, a calm starting point for a nagging concern.",
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
