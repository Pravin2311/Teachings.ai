#!/usr/bin/env python3
"""Fixes title/description length across the remaining root-level pages
(math/phonics/grammar games, hub pages). Bespoke pages, hand-trimmed
per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "Grammar.html": (
        "Grammar Fun: Nouns & Verbs Game for Kids | Teachings.AI",
        "Fun interactive grammar game to learn nouns and verbs, with instant feedback and simple examples. Part of Teachings.AI's learning modules for kids.",
    ),
    "counting.html": (
        "Counting with Objects: A Math Game for Kids | Teachings.AI",
        "Interactive counting game for kids 3-7. Count animals, fruits, and birds to build number sense and early math skills for preschool learners.",
    ),
    "downloads.html": (
        "Free Printable Worksheets for Preschool | Teachings.AI",
        "Download 100% free printable worksheets for preschool and kindergarten kids. Fun activities: alphabets, numbers, math, coloring, and shapes.",
    ),
    "games.html": (
        "Free Kids Learning Games: Sorting & Matching | Teachings.AI",
        "Interactive sorting and matching games for kids: odd/even, alphabets, numbers, animals, and more. Fun learning for ages 3-10 at Teachings.AI.",
    ),
    "index.html": (
        "Kids Learning: Alphabets, Numbers & Fun Worksheets",
        "Teachings.AI: Interactive learning web app for kids aged 3-10. Engaging games and activities to learn numbers, alphabets, animals, and colors.",
    ),
    "math.html": (
        "Simple Math for Kids: Addition & Subtraction | Teachings.AI",
        "Teachings.AI: Fun and simple math exercises for kids. Practice addition and subtraction problems for early learners with instant, friendly feedback.",
    ),
    "mirror-words-learning.html": (
        "Reflection Words: A Playful Kids Edition Game to Try",
        "Fun and colorful reflection words game for kids! Children learn how words look when reversed (NET to TEN) through playful, interactive options.",
    ),
    "odd-even.html": (
        "Odd & Even Numbers Game for Kids Too | Teachings.AI",
        "Teach your kids to identify odd and even numbers with this fun, interactive math game. Includes voice feedback and educational tips for kids.",
    ),
    "patterns.html": (
        "Patterns & Sequences for Kids: A Fun Game | Teachings.AI",
        "Teachings.AI: Fun patterns and sequences game for kids to learn and identify patterns using emojis and shapes, building early math thinking.",
    ),
    "phonic-letter-sound.html": (
        None,
        "Interactive phonics A-Z letter-sound correspondence game for kids. Learn phonics with drag-and-drop activities, audio sounds, and fun pictures.",
    ),
    "phonic-numbers.html": (
        "Number Sound Match Game for Kids Too | Teachings.AI",
        None,
    ),
    "phonic-rhyming.html": (
        "Rhyming & Listening Game for Kids Too | Teachings.AI",
        "A rhyming and listening game for kids ages 3-7. Hear a word, then pick the picture that rhymes with it to build phonemic awareness for reading.",
    ),
    "phonic-segmenting.html": (
        None,
        "Fun phonics game for kids! Learn to read by building words with drag-and-drop letters, perfect for preschool and kindergarten early readers.",
    ),
    "phonic-words.html": (
        "Sound & Blend: Learn Phonics Game Too | Teachings.AI",
        None,
    ),
    "phonics.html": (
        "Kids Phonics Games: Sound Blending & More | Teachings.AI",
        "Free phonics games for kids: sound blending, letter-sound matching, phonic numbers, and word building for preschool and kindergarten learners.",
    ),
    "rhyming.html": (
        None,
        "Interactive rhyming words game for kids. Match words that rhyme, hear audio, and build phonics skills for preschool and kindergarten readers.",
    ),
    "sentences.html": (
        "Build Simple Sentences: A Learning Game | Teachings.AI",
        "Interactive sentence builder for kids 3-7. Boost early reading, grammar, and word order skills with fun, no-distractor sentence puzzles for kids.",
    ),
    "shapes.html": (
        "Basic Shapes Matching Game for Kids | Teachings.AI",
        "Learn basic shapes with Teachings.AI — fun and interactive shape matching games for kids that build shape recognition and visual thinking skills.",
    ),
    "tracing-letters-and-numbers.html": (
        None,
        "Fun and interactive tracing app for kids to learn ABC letters and numbers with smooth drawing and glowing effects for toddlers and preschool.",
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
