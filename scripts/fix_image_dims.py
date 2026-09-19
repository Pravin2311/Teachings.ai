#!/usr/bin/env python3
"""Adds width/height attributes to <img> tags that are missing them, reading
the real pixel dimensions from the actual image file (local repo path, or
the jsdelivr CDN mirror of this same repo, which resolves back to a local
file). Explicit width/height prevents layout shift (CLS) as images load.

Images whose source file can't be resolved locally are left untouched and
reported for manual follow-up.
"""
import glob
import os
import re
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow (PIL) is required: pip install Pillow")
    raise

SKIP_DIRS = ("mockups/", ".git/", "node_modules/")
SKIP_FILES = {"furits-vegetables-sorting.html"}
CDN_PREFIX = "https://cdn.jsdelivr.net/gh/Pravin2311/Teachings.ai@main/"

IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
SRC_RE = re.compile(r'src\s*=\s*"([^"]*)"', re.I)

_dim_cache = {}


def get_attr(tag, name):
    m = re.search(rf'{name}\s*=\s*"([^"]*)"', tag, re.I)
    return m.group(1) if m else None


def resolve_local_path(src, html_file):
    if src.startswith(CDN_PREFIX):
        rel = src[len(CDN_PREFIX):]
        return rel if os.path.isfile(rel) else None
    if src.startswith("http"):
        return None
    if src.startswith("/"):
        rel = src.lstrip("/")
        return rel if os.path.isfile(rel) else None
    # relative to the html file's own directory
    base_dir = os.path.dirname(html_file)
    candidate = os.path.normpath(os.path.join(base_dir, src))
    return candidate if os.path.isfile(candidate) else None


def get_dims(local_path):
    if local_path in _dim_cache:
        return _dim_cache[local_path]
    try:
        with Image.open(local_path) as im:
            dims = im.size
    except Exception:
        dims = None
    _dim_cache[local_path] = dims
    return dims


def process_file(fname, dry_run):
    src_text = open(fname, encoding="utf-8").read()
    new_text = src_text
    changed = 0
    unresolved = []

    for tag in IMG_RE.findall(src_text):
        w, h = get_attr(tag, "width"), get_attr(tag, "height")
        if w and h:
            continue
        sm = SRC_RE.search(tag)
        if not sm:
            continue
        src = sm.group(1)
        local_path = resolve_local_path(src, fname)
        if not local_path:
            unresolved.append(src)
            continue
        dims = get_dims(local_path)
        if not dims:
            unresolved.append(src)
            continue
        width, height = dims
        new_tag = tag
        if not w:
            new_tag = re.sub(r"<img\b", f'<img width="{width}"', new_tag, count=1)
        if not h:
            new_tag = re.sub(r"<img\b", f'<img height="{height}"', new_tag, count=1)
        if new_tag != tag:
            new_text = new_text.replace(tag, new_tag, 1)
            changed += 1

    if changed:
        print(f"[{'DRY' if dry_run else 'OK'}] {fname}: +{changed} dims" + (f"  (unresolved: {len(unresolved)})" if unresolved else ""))
        if not dry_run:
            with open(fname, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_text)
    elif unresolved:
        print(f"[UNRESOLVED ONLY] {fname}: {len(unresolved)} images -> {unresolved[:3]}")

    return changed, len(unresolved)


def main():
    dry_run = "--dry-run" in sys.argv
    files = [f for f in glob.glob("**/*.html", recursive=True) if not f.startswith(SKIP_DIRS)]
    files = [f for f in files if f.replace("\\", "/") not in SKIP_FILES]
    files.sort()

    total_changed, total_unresolved = 0, 0
    for f in files:
        c, u = process_file(f, dry_run)
        total_changed += c
        total_unresolved += u

    print(f"\ntotal_images_fixed={total_changed} total_unresolved={total_unresolved} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
