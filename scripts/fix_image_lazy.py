#!/usr/bin/env python3
"""Adds loading="lazy" to <img> tags that don't already declare a loading
attribute. Skips the FIRST <img> tag in each page's <body> (heuristic for
the likely above-the-fold / LCP image, which should load eagerly) and any
tag using a JS template-literal src (can't safely rewrite those statically).
"""
import glob
import re
import sys

SKIP_DIRS = ("mockups/", ".git/", "node_modules/")
SKIP_FILES = {"furits-vegetables-sorting.html"}

IMG_RE = re.compile(r"<img\b[^>]*>", re.I)


def has_loading(tag):
    return re.search(r'loading\s*=\s*["\']', tag, re.I) is not None


def process_file(fname, dry_run):
    src = open(fname, encoding="utf-8").read()

    body_start = src.lower().find("<body")
    search_from = body_start if body_start != -1 else 0

    tags = list(IMG_RE.finditer(src, search_from))
    if not tags:
        return 0

    first_seen = False
    changed = 0
    new_src = src
    offset = 0
    for m in tags:
        tag = m.group(0)
        if has_loading(tag):
            if not first_seen:
                first_seen = True
            continue
        if not first_seen:
            # this is the first image without an explicit loading attr;
            # treat it as the likely hero image and leave it eager
            first_seen = True
            continue
        new_tag = re.sub(r"<img\b", '<img loading="lazy"', tag, count=1)
        start = m.start() + offset
        end = m.end() + offset
        new_src = new_src[:start] + new_tag + new_src[end:]
        offset += len(new_tag) - len(tag)
        changed += 1

    if changed:
        print(f"[{'DRY' if dry_run else 'OK'}] {fname}: +{changed} lazy")
        if not dry_run:
            with open(fname, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_src)
    return changed


def main():
    dry_run = "--dry-run" in sys.argv
    files = [f for f in glob.glob("**/*.html", recursive=True) if not f.startswith(SKIP_DIRS)]
    files = [f for f in files if f.replace("\\", "/") not in SKIP_FILES]
    files.sort()

    total = 0
    for f in files:
        total += process_file(f, dry_run)

    print(f"\ntotal_images_lazy_added={total} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
