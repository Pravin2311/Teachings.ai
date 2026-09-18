#!/usr/bin/env python3
"""Fixes title length across learn/animals/*.html (excluding index.html); only the
6 pages whose description also ran short (cat, cow, dog, horse, lion, tiger) get
a description change too -- the rest were already in range."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

# slug -> (Name, Plural, use_long_suffix)
NAMES = {
    "bear": ("Bear", "Bears", True), "cat": ("Cat", "Cats", True),
    "cow": ("Cow", "Cows", True), "dog": ("Dog", "Dogs", True),
    "dolphin": ("Dolphin", "Dolphins", False), "donkey": ("Donkey", "Donkeys", False),
    "elephant": ("Elephant", "Elephants", False), "giraffe": ("Giraffe", "Giraffes", False),
    "horse": ("Horse", "Horses", True), "kangaroo": ("Kangaroo", "Kangaroos", False),
    "lion": ("Lion", "Lions", True), "monkey": ("Monkey", "Monkeys", False),
    "penguin": ("Penguin", "Penguins", False), "tiger": ("Tiger", "Tigers", True),
    "zebra": ("Zebra", "Zebras", True),
}

NEW_DESCS = {
    "cat": "Learn about cats for kids: how they purr, what they eat, and fun cat facts to share! Perfect for preschoolers and kindergarten animal studies.",
    "cow": "Learn about cows for kids: what they give us, how they eat, and fun cow facts to explore! Perfect for preschoolers and kindergarten animal studies.",
    "dog": "Learn about dogs for kids: how they bark, what they eat, and fun dog facts to share! Perfect for preschoolers and kindergarten animal studies.",
    "horse": "Learn about horses for kids: how they run, what they eat, and fun horse facts to explore! Perfect for preschoolers and kindergarten animal studies.",
    "lion": "Learn about lions for kids: how they roar, what they eat, and fun lion facts to explore! Perfect for preschoolers and kindergarten animal studies.",
    "tiger": "Learn about tigers for kids: how they stripe, what they eat, and fun tiger facts! Perfect for preschoolers and kindergarten animal studies too.",
}


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for slug, (name, plural, long_suffix) in NAMES.items():
        fname = f"learn/animals/{slug}.html"
        suffix = "with Pictures & Facts" if long_suffix else "with Fun Facts"
        new_title = f"{name} for Kids: Learn About {plural} {suffix}"
        new_desc = NEW_DESCS.get(slug)

        if not (TITLE_MIN <= len(new_title) <= TITLE_MAX):
            print(f"[BAD TITLE LEN {len(new_title)}] {fname}: {new_title}")
            bad += 1
            continue
        if new_desc is not None and not (DESC_MIN <= len(new_desc) <= DESC_MAX):
            print(f"[BAD DESC LEN {len(new_desc)}] {fname}: {new_desc}")
            bad += 1
            continue

        ok += 1
        print(f"[{'DRY' if dry_run else 'OK'}] {fname} title={len(new_title)} desc={len(new_desc) if new_desc else 'unchanged'}")
        if dry_run:
            continue

        src = open(fname, encoding="utf-8").read()
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
