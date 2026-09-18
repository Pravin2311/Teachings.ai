#!/usr/bin/env python3
"""Fixes title/description length across Blog/*.html. Bespoke announcement
posts, hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "Blog/educational-games-and-worksheets-launch.html": (
        "Teachings.AI Official Launch: Free Preschool Games",
        "Teachings.AI launches free preschool learning games! Fun online activities for kids ages 3-6 — alphabet games, number sorting, and worksheets.",
    ),
    "Blog/human-body-organs-learning.html": (
        "Discover Human Organs with a Fun Scratch Card Game",
        "Explore the human body with an interactive scratch card game on Teachings.AI. Learn about major organs like the brain, heart, and lungs. Free for kids!",
    ),
    "Blog/index.html": (
        "Blog: Tips, Updates & Fun Learning Ideas for Kids Too",
        "Teachings.AI blog — tips, updates, and fun learning ideas for parents, teachers, and kids exploring our free educational games and worksheets.",
    ),
    "Blog/new-phonics-games-update.html": (
        "New Phonics Games: Sound & Blend + Letter Match Too",
        "Discover two new phonics games on Teachings.AI: Sound & Blend and Letter-Sound Correspondence. Free interactive learning for early readers to enjoy!",
    ),
    "Blog/new-scratch-card-games.html": (
        "New Scratch Card Games: Fantasy, Gadgets & Planets",
        "Discover exciting new scratch card games at Teachings.AI: explore Fantasy Worlds, Electronic Gadgets, Planets, and Scientists. Free and fun for kids!",
    ),
    "Blog/numbers-interactive-games-for-counting-matching-sorting.html": (
        "Learn Numbers: Interactive Counting & Matching Games",
        "Free, fun number activities for kids: scratch-card counting with audio, drag-and-drop matching, and an odd/even identifier for young learners.",
    ),
    "Blog/numbers-worksheets-for-tracing-colouring-matching.html": (
        "Free Numbers Worksheets: Coloring, Tracing & Matching",
        "Download free printable numbers worksheets for kids. Fun coloring, tracing, and matching activities to help preschoolers learn numbers 0-10.",
    ),
    "Blog/phonics-letter-sounds-fantasy-world-pages.html": (
        "New Phonics Pages + Fantasy World Characters Added",
        "Teachings.AI adds 21 phonics letter-sound reading pages (Ball to Yak) and 7 Fantasy World character pages for early-reading practice at home.",
    ),
    "Blog/scratch-games-to-learn-alphabets-numbers-aminals-shapes.html": (
        "Fun Scratch Games for Kids: Alphabets, Animals & More",
        "Discover engaging scratch card games at Teachings.AI for learning alphabets, animals, birds, fruits, vegetables, and body parts. Free and ad-free!",
    ),
    "Blog/vehicles-electronics-countries-learning-pages.html": (
        "New Vehicles, Electronics & Countries Pages Added Too",
        "Teachings.AI adds 56 new learning pages: fire trucks to fighter jets, cameras to solar panels, and Germany to the UAE, with fun facts for kids.",
    ),
    "Blog/world-of-learning-hub-expansion.html": (
        "7 New Learning Topics: Shapes, Numbers & Scientists",
        "Teachings.AI's World of Learning hub just grew by 7 topics — Shapes, Numbers, Scientists, Plants, Body Organs, and Community Helpers, free for kids.",
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
