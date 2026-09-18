#!/usr/bin/env python3
"""Fixes title/description length across learn/organs/*.html (excluding index.html)."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "learn/organs/brain.html": (
        "Brain for Kids: How They Help Your Body & Fun Facts",
        "Learn about the Brain! Fun, simple facts about thinking, remembering, and controlling your whole body. Great for kindergarten science learners.",
    ),
    "learn/organs/eye.html": (
        "Eyes for Kids: How They Help Your Body & Fun Facts",
        "Learn about the Eyes! Fun, simple facts about seeing the colors, shapes, and people around you. Great for preschool and kindergarten science.",
    ),
    "learn/organs/heart.html": (
        "Heart for Kids: How They Help Your Body & Fun Facts",
        "Learn about the Heart! Fun, simple facts about how it pumps blood all around your body. Great for preschool and kindergarten science learners.",
    ),
    "learn/organs/intestine.html": (
        "Intestines for Kids: How They Help Your Body & Facts",
        "Learn about the Intestines! Fun, simple facts about absorbing nutrients from food and moving waste along your digestive system. Great for kindergarten.",
    ),
    "learn/organs/kidney.html": (
        "Kidneys for Kids: How They Help Your Body & Fun Facts",
        "Learn about the Kidneys! Fun, simple facts about filtering your blood and making urine. Great for preschool and kindergarten science learners.",
    ),
    "learn/organs/liver.html": (
        "Liver for Kids: How They Help Your Body & Fun Facts",
        "Learn about the Liver! Fun, simple facts about cleaning your blood and helping digest food. Great for preschool and kindergarten science learners.",
    ),
    "learn/organs/lungs.html": (
        "Lungs for Kids: How They Help Your Body & Fun Facts",
        "Learn about the Lungs! Fun, simple facts about breathing in fresh air and breathing out used air. Great for preschool and kindergarten science.",
    ),
    "learn/organs/lymph-node.html": (
        "Lymph Nodes for Kids: How They Help Your Body & Facts",
        "Learn about the Lymph Nodes! Fun, simple facts about helping your body fight off germs. Great for preschool and kindergarten science learners.",
    ),
    "learn/organs/muscle.html": (
        "Muscles for Kids: How They Help Your Body & Fun Facts",
        "Learn about the Muscles! Fun, simple facts about helping your body move, run, and jump. Great for preschool and kindergarten science learners.",
    ),
    "learn/organs/stomach.html": (
        "Stomach for Kids: How They Help Your Body & Fun Facts",
        "Learn about the Stomach! Fun, simple facts about how it breaks down the food you eat every day. Great for preschool and kindergarten science.",
    ),
    "learn/organs/teeth.html": (
        "Teeth for Kids: How They Help Your Body & Fun Facts",
        "Learn about the Teeth! Fun, simple facts about biting, chewing, and taking care of your smile. Great for preschool and kindergarten science learners.",
    ),
}


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for fname, (new_title, new_desc) in CHANGES.items():
        if not (TITLE_MIN <= len(new_title) <= TITLE_MAX) or not (DESC_MIN <= len(new_desc) <= DESC_MAX):
            print(f"[BAD LEN] {fname} title={len(new_title)} desc={len(new_desc)}")
            bad += 1
            continue
        ok += 1
        print(f"[{'DRY' if dry_run else 'OK'}] {fname} title={len(new_title)} desc={len(new_desc)}")
        if dry_run:
            continue
        src = open(fname, encoding="utf-8").read()
        tm = TITLE_RE.search(src)
        src = src[: tm.start(1)] + new_title.replace("&", "&amp;") + src[tm.end(1):]
        dm = DESC_RE.search(src)
        src = src[: dm.start(3)] + new_desc.replace("&", "&amp;") + src[dm.end(3):]
        with open(fname, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
    print(f"\nok={ok} bad={bad} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
