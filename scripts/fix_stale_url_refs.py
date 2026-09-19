#!/usr/bin/env python3
"""Sweeps each affected file for every remaining occurrence of its OLD,
pre-rename URL (og:url, JSON-LD breadcrumb items, JSON-LD "url"/"about.url"
fields, etc.) and replaces it with the page's current, correct URL. The
canonical <link> tags were already fixed by fix_stale_canonicals.py; this
catches the rest (og:url and any JSON-LD self-references) via a scoped
find-and-replace within each file.
"""
import sys

# file -> list of (old_url_fragment, new_url_fragment) to replace, in order
REPLACEMENTS = {}

BASE = "https://www.teachings.ai/"

for name in ["duck", "eagle", "flamingo", "hen", "hummingbird", "owl", "parrot", "peacock", "pigeon", "sparrow"]:
    REPLACEMENTS[f"learn/birds/{name}.html"] = [
        (f"{BASE}learn/animals/birds/{name}.html", f"{BASE}learn/birds/{name}.html"),
    ]

for name in ["arms", "ears", "eyes", "feet", "hands", "head", "index", "legs", "mouth", "nose", "stomach"]:
    REPLACEMENTS[f"learn/body-parts/{name}.html"] = [
        (f"{BASE}learn/bodyparts/{name}.html", f"{BASE}learn/body-parts/{name}.html"),
    ]

REPLACEMENTS["learn/fruits/grapes.html"] = [
    (f"{BASE}learn/fruits/grape.html", f"{BASE}learn/fruits/grapes.html"),
]
REPLACEMENTS["learn/vehicles/ships.html"] = [
    (f"{BASE}learn/vehicles/boat.html", f"{BASE}learn/vehicles/ships.html"),
]
REPLACEMENTS["phonic-segmenting.html"] = [
    (f"{BASE}phonics-game", f"{BASE}phonic-segmenting.html"),
]
REPLACEMENTS["phonic-words.html"] = [
    (f"{BASE}phonics/sound-and-blend.html", f"{BASE}phonic-words.html"),
]
REPLACEMENTS["phonics.html"] = [
    (f'content="{BASE}games.html"', f'content="{BASE}phonics.html"'),
]
REPLACEMENTS["privacy-policy.html"] = [
    (f"{BASE}privacy.html", f"{BASE}privacy-policy.html"),
]


def main():
    dry_run = "--dry-run" in sys.argv
    total_subs = 0
    for fname, pairs in REPLACEMENTS.items():
        src = open(fname, encoding="utf-8").read()
        new_src = src
        file_subs = 0
        for old, new in pairs:
            count = new_src.count(old)
            if count:
                new_src = new_src.replace(old, new)
                file_subs += count
        if file_subs:
            print(f"[{'DRY' if dry_run else 'OK'}] {fname}: {file_subs} replacement(s)")
            total_subs += file_subs
            if not dry_run:
                with open(fname, "w", encoding="utf-8", newline="\n") as f:
                    f.write(new_src)
        else:
            print(f"[NONE LEFT] {fname}")
    print(f"\ntotal_substitutions={total_subs} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
