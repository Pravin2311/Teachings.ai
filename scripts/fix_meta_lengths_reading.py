#!/usr/bin/env python3
"""Fixes title/description length across reading/*.html. Bespoke articles,
hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "reading/audiobooks-and-when-they-count-as-reading.html": (
        None,
        "What audiobooks genuinely build versus what they don't, when they're a good substitute for print reading, and how to combine both formats well.",
    ),
    "reading/best-childrens-books-by-age.html": (
        "Best Children's Books by Age: A Curated Reading List",
        "A curated list of well-loved children's books organized by age band, from board books through middle grade, with tips to find your own favorites.",
    ),
    "reading/best-phonics-readers-and-decodable-books.html": (
        "Best Phonics Readers & Decodable Book Series to Try",
        "A curated list of well-known decodable and phonics reader series for beginning readers, with guidance on what makes a book genuinely decodable.",
    ),
    "reading/building-reading-stamina.html": (
        "Building Reading Stamina: Short Bursts to Sustained",
        "How to grow a child's reading stamina gradually — starting from short, comfortable bursts and building toward longer sustained reading sessions.",
    ),
    "reading/daily-phonics-practice-routine.html": (
        None,
        "How to structure a short, sustainable daily phonics practice routine — what to include, how long it should take, and how to stay consistent.",
    ),
    "reading/family-read-aloud-habit.html": (
        None,
        "How to build a lasting family read-aloud habit — picking the right time, handling reluctant listeners, and why reading aloud still matters most.",
    ),
    "reading/how-to-choose-a-phonics-program.html": (
        "How to Choose a Phonics Program That Actually Works",
        "Systematic vs. embedded phonics explained, key questions to ask before choosing a program, and red flags to watch for in any phonics curriculum.",
    ),
    "reading/index.html": (
        "Reading Library: Curated Book Lists & Reading Guidance",
        None,
    ),
    "reading/phonics-patterns-reference-guide.html": (
        "Phonics Patterns Reference Guide for Parents & Teachers",
        "A quick-reference chart of common phonics patterns — digraphs, blends, vowel teams, silent e, and r-controlled vowels — with example words for kids.",
    ),
    "reading/reading-comprehension-questions-to-ask.html": (
        None,
        "A practical toolkit of reading comprehension questions organized by thinking level — recall, inference, connection, and evaluation for any book.",
    ),
    "reading/reluctant-reader-strategies.html": (
        "Reluctant Reader Strategies That Actually Work Well",
        "Practical strategies for a child who can read but resists it — finding the actual barrier, low-pressure entry points, and what usually backfires.",
    ),
    "reading/sight-words-vs-phonics-how-they-work-together.html": (
        "Sight Words vs. Phonics: How They Work Well Together",
        "Why sight words and phonics aren't competing methods but two tools for two different problems, and how a reading approach typically uses both.",
    ),
    "reading/understanding-reading-levels.html": (
        "Understanding Reading Levels: A Parent's Guide Too",
        "What reading levels actually measure, the difference between common leveling systems, and how to choose a genuinely 'just right' book for your child.",
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
