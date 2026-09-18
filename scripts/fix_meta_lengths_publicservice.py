#!/usr/bin/env python3
"""Fixes title/description length across learn/publicservice/*.html (excluding index.html)."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

NEW_TITLES = {
    "airport": "Airport for Kids – Community Helpers & Fun Facts Too",
    "hospital": "Hospital for Kids – Community Helpers & Fun Facts Too",
    "library": "Library for Kids – Community Helpers & Fun Facts Too",
    "museum": "Museum for Kids – Community Helpers & Fun Facts Too",
    "park": "Park for Kids – Community Helpers & Fun Facts to Learn",
    "school": "School for Kids – Community Helpers & Fun Facts Too",
}

NEW_DESCS = {
    "airport": "Learn about the Airport and the pilots who work there! Discover how they help planes take off, land, and carry passengers safely each and every day.",
    "cityhall": "Learn about the City Hall and the mayor and city workers who work there! Discover how they make decisions and provide services for the city.",
    "firestation": "Learn about the Fire Station and the firefighters who work there! Discover how they put out fires and rescue people in danger every single day.",
    "hospital": "Learn about the Hospital and the doctors and nurses who work there! Discover how they help sick or hurt people feel better again very quickly.",
    "library": "Learn about the Library and the librarians who work there! Discover how they help people find, borrow, and enjoy good books every single day.",
    "museum": "Learn about the Museum and the curators and guides who work there! Discover how they show and protect history, art, and science exhibits daily.",
    "park": "Learn about the Park and the park rangers who work there! Discover how they take care of green spaces where people play and relax together daily.",
    "policestation": "Learn about the Police Station and the officers who work there! Discover how they keep our neighborhoods safe every single day and every night.",
    "postoffice": "Learn about the Post Office and the mail carriers who work there! Discover how they deliver letters and packages to homes every single busy day.",
    "school": "Learn about the School and the teachers and students who learn there! Discover how they teach reading, writing, and lots of exciting new things.",
}

ALL_SLUGS = ["airport", "cityhall", "firestation", "hospital", "library", "museum", "park", "policestation", "postoffice", "school"]


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for slug in ALL_SLUGS:
        fname = f"learn/publicservice/{slug}.html"
        new_title = NEW_TITLES.get(slug)
        new_desc = NEW_DESCS.get(slug)
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
