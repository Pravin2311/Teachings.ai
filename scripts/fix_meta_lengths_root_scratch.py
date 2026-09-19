#!/usr/bin/env python3
"""Fixes title/description length across the root-level scratch-reveal game
pages. Bespoke pages, hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "alphabets.html": (
        "Learn Alphabets: A-Z Interactive Game | Teachings.AI",
        "Interactive alphabet game for kids: scratch to reveal letters A-Z, hear pronunciation, and learn with example words. Fun and perfect for preschool.",
    ),
    "animals.html": (
        "Learn Animal Names & Sounds: A Game for Kids | Teachings.AI",
        "Interactive animal learning game for kids 3-7. Discover wild, farm, and jungle animals with sounds, names, and scratch-to-reveal fun for preschool.",
    ),
    "birds.html": (
        "Learn Bird Names & Sounds: A Game for Kids | Teachings.AI",
        "Interactive bird learning game for kids 3-7. Discover common birds with sounds, names, and scratch-to-reveal fun for preschool and kindergarten.",
    ),
    "bodyparts.html": (
        None,
        "Interactive body parts game for kids 3-7. Discover head, shoulders, elbows, and toes with fun scratch-to-reveal gameplay for preschool science.",
    ),
    "colors.html": (
        None,
        "Interactive color learning game for kids 3-7. Discover primary and secondary colors with fun scratch-to-reveal gameplay for preschool learners.",
    ),
    "countries.html": (
        None,
        "Interactive scratch-to-reveal game where kids learn country names and geography facts. Fun learning for preschool and kindergarten by Teachings.AI.",
    ),
    "electronic-gadgets.html": (
        "Learn Electronic Gadgets: Fun Scratch Game | Teachings.AI",
        "Interactive scratch-and-learn game to teach kids about electronic gadgets. Reveal and hear names like laptop, tablet, and phone in this fun module.",
    ),
    "fantasy-world.html": (
        "Learn Fantasy Characters: Fun Scratch Game | Teachings.AI",
        None,
    ),
    "flags-of-the-countries.html": (
        "Learn Flags of the Countries: Scratch Game | Teachings.AI",
        "Interactive scratch-to-reveal game where kids learn world flags and geography. Fun flag-recognition learning for preschool and kindergarten kids.",
    ),
    "fruits.html": (
        "Learn Fruits: Scratch-to-Reveal Game for Kids | Teachings.AI",
        "Interactive module for kids to learn about different fruits. Scratch to reveal fruit images, hear their names, and build early vocabulary skills.",
    ),
    "nature-explorer.html": (
        None,
        "Interactive game to teach kids about nature and wildlife. Scratch to reveal and hear names of plants and animals in this fun learning module.",
    ),
    "numbers.html": (
        "Learn Numbers: Scratch-to-Reveal Game | Teachings.AI",
        "Interactive module for kids to learn numbers 0-10. Scratch to reveal fun images and hear number pronunciations to build early counting skills.",
    ),
    "organs.html": (
        "Learn Human Organs: Interactive Anatomy Game | Teachings.AI",
        "Interactive human organs learning game for kids 6-10. Discover heart, lungs, brain, and stomach with scratch-to-reveal fun for elementary science.",
    ),
    "planets.html": (
        None,
        "Interactive scratch-to-reveal game to teach kids the names of planets in our solar system, with audio support for young space explorers to enjoy.",
    ),
    "plants.html": (
        "Learn About Plants: A Fun Interactive Module | Teachings.AI",
        "Interactive plant learning module for preschool and kindergarten kids. See real plant images, hear names, and explore nature with audio support.",
    ),
    "publicservice.html": (
        "Public Service Institutions: A Learning App | Teachings.AI",
        "Interactive module for kids to learn about public service institutions: police, fire station, hospital, and post office. Fun and audio-supported.",
    ),
    "scientists.html": (
        "Learn About Scientists: Fun Scratch Game | Teachings.AI",
        "Interactive scratch-to-reveal game to teach kids about famous scientists like Marie Curie and Albert Einstein, with audio support for learners.",
    ),
    "vegetables.html": (
        None,
        "Interactive scratch-to-reveal game to teach kids about healthy vegetables like carrot, broccoli, and tomato, with audio support for young kids.",
    ),
    "vehicles.html": (
        "Learn Vehicles: Sounds and Names Game | Teachings.AI",
        "Interactive vehicle learning game for kids. Scratch to reveal and hear car, truck, bus, and other vehicle names and sounds for young learners.",
    ),
    "word-matching.html": (
        "Word Matching Game for Kids: Animals & Birds | Teachings.AI",
        "Interactive word matching game for kids. Match words with pictures of animals, birds, and fruits for fun preschool vocabulary building practice.",
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
