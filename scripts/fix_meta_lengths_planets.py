#!/usr/bin/env python3
"""Fixes title/description length across learn/planets/*.html (excluding index.html)."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

NEW_TITLES = {
    "earth": "Earth for Kids – Facts, Size, Moon & Life to Discover",
    "mercury": "Mercury for Kids – The Fastest & Smallest Planet Too",
    "moon": "Moon for Kids – Phases, Craters & Apollo Missions Too",
    "pluto": "Pluto for Kids – The Dwarf Planet with an Icy Heart",
    "uranus": "Uranus for Kids – The Sideways Ice Giant Planet Too",
}

NEW_DESCS = {
    "earth": "Learn all about Earth for kids! Discover why it has life, its size, distance from the Sun, and fun facts about the Moon for young space learners.",
    "jupiter": "Learn all about Jupiter for kids! Discover why it's the largest planet, the Great Red Spot storm, and its many moons like Europa and Io too.",
    "mars": "Learn all about Mars for kids! Discover why it's red, its giant volcanoes, famous rovers like Curiosity, and if humans can live there someday.",
    "mercury": "Learn all about Mercury for kids! Discover why it's the smallest planet, its extreme temperatures, fast orbit, and cratered rocky surface today.",
    "moon": "Learn all about the Moon for kids! Discover why it changes shape, its craters, low gravity, Apollo astronauts, and how it causes ocean tides.",
    "neptune": "Learn all about Neptune for kids! Discover its supersonic winds, Great Dark Spot, icy composition, and its mysterious moon called Triton too.",
    "pluto": "Learn all about Pluto for kids! Discover why it's a dwarf planet, its icy heart shape, giant moon Charon, and life in the Kuiper Belt today.",
    "saturn": "Learn all about Saturn for kids! Discover its beautiful icy rings, why it could float in water, and its mysterious foggy moon called Titan today.",
    "uranus": "Learn all about Uranus for kids! Discover why it spins on its side, its icy blue-green composition, cold temperatures, and its faint rings today.",
    "venus": "Learn all about Venus for kids! Discover why it's the hottest planet, its thick clouds, backward spin, and why it's called Earth's twin too.",
}

ALL_SLUGS = ["earth", "jupiter", "mars", "mercury", "moon", "neptune", "pluto", "saturn", "uranus", "venus"]


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for slug in ALL_SLUGS:
        fname = f"learn/planets/{slug}.html"
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
