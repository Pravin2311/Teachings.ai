#!/usr/bin/env python3
"""Fixes title/description length across games-library/*.html. Bespoke
articles, hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "games-library/building-a-weekly-game-rotation.html": (
        "Building a Weekly Game Rotation for Multiple Skills",
        "A simple weekly rotation strategy for mixing number, letter, matching, and pattern games so a child practices a range of skills, not just one.",
    ),
    "games-library/how-long-should-learning-game-screen-time-be.html": (
        None,
        "How long a learning game session should realistically run by age, the signs a child has hit a natural stopping point, and why longer isn't better.",
    ),
    "games-library/how-to-choose-a-good-educational-game.html": (
        None,
        "What separates a genuinely educational game from entertainment wearing an educational label — feedback loops, real skill progression, and red flags.",
    ),
    "games-library/index.html": (
        "Learning Games Library: A Skill-Based Guide to Games",
        "A skill-based guide to Teachings.ai's free learning games — what each game builds, why matching and sorting mechanics teach, and how to choose one.",
    ),
    "games-library/learning-games-by-age-and-skill.html": (
        "Learning Games by Age and Skill: A Complete Guide Too",
        "A skill-based map of free learning games for kids — matching, sorting, numbers, letters, and more — organized by skill and the age it fits best.",
    ),
    "games-library/multiplayer-games-for-siblings-and-friends.html": (
        None,
        "How turn-based learning games between siblings or friends build cooperation and gracious losing alongside skills, and how to set up fair play.",
    ),
    "games-library/screen-free-games-that-build-the-same-skills.html": (
        None,
        "Offline, screen-free activities that build the same skills as our matching, sorting, and pattern games — using household objects you already have.",
    ),
    "games-library/turning-game-time-into-a-learning-conversation.html": (
        "Turning Game Time Into a Learning Conversation Too",
        "Simple questions and comments that extend a learning game beyond the screen, turning a few minutes of play into a real conversation with your child.",
    ),
    "games-library/why-matching-and-sorting-games-work.html": (
        "Why Matching and Sorting Games Build Real Skills Too",
        "The learning science behind common game mechanics — why matching builds memory, sorting builds classification, and feedback helps kids self-correct.",
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
