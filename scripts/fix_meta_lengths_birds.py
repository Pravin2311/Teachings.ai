#!/usr/bin/env python3
"""Fixes title/description length across learn/birds/*.html (excluding index.html)."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

TITLES = {
    "duck": "Duck for Kids: Learn About Ducks with Pictures & Facts",
    "eagle": "Eagle for Kids: Learn About Eagles with Pictures & Facts",
    "flamingo": "Flamingo for Kids: Learn About Flamingos with Fun Facts",
    "hen": "Hen for Kids: Learn About Hens with Pictures & Facts",
    "hummingbird": "Hummingbird for Kids: Flight Speed, Flowers & Facts",
    "owl": "Owl for Kids: Learn About Owls with Pictures & Facts",
    "parrot": "Parrot for Kids: Learn About Parrots with Fun Facts",
    "peacock": "Peacock for Kids: Learn About Peacocks with Fun Facts",
    "pigeon": "Pigeon for Kids: Learn About Pigeons with Fun Facts",
    "sparrow": "Sparrow for Kids: Learn About Sparrows with Fun Facts",
}

NEW_DESCS = {
    "duck": "Learn all about ducks for kids: what they eat, where they live, how they swim, and fun duck facts! Perfect for preschool and kindergarten kids.",
    "eagle": "Learn all about eagles for kids: where they nest, what they eat, how they fly, and fun eagle facts! Perfect for preschool and kindergarten kids.",
    "flamingo": "Learn all about flamingos for kids: why they’re pink, how they stand on one leg, and fun flamingo facts! Perfect for preschoolers and kindergarten.",
    "hummingbird": "Learn all about hummingbirds for kids: how fast they fly, what flowers they like, and fun facts! Perfect for preschoolers and kindergarten studies.",
    "owl": "Learn all about owls for kids: why they hunt at night, how they turn their heads, and fun owl facts! Perfect for preschoolers and kindergarten.",
    "peacock": "Learn all about peacocks for kids: why they spread their tail, what colors they have, and fun peacock facts! Perfect for preschool and kindergarten.",
}


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for slug, new_title in TITLES.items():
        fname = f"learn/birds/{slug}.html"
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
