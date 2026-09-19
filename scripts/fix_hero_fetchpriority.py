"""
Adds fetchpriority="high" to each page's hero/LCP image -- the same
first-<img>-in-<body> heuristic already used by fix_image_lazy.py to
decide which image NOT to lazy-load. Google explicitly recommends this
attribute for the actual LCP element: it tells the browser to fetch that
image before other same-priority resources, directly improving LCP (a
Core Web Vitals ranking signal) instead of just relying on load order.

Skips: images that already declare fetchpriority, and any tag using a
JS template-literal src (can't safely target those).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
DRY_RUN = "--dry-run" in sys.argv

IMG_RE = re.compile(r"<img\b[^>]*>", re.I)


def has_attr(tag, name):
    return re.search(rf'{name}\s*=\s*["\']', tag, re.I) is not None


def main():
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                src = fh.read()

            if 'http-equiv="refresh"' in src[:500]:
                continue  # redirect stub, no real hero image

            body_start = src.lower().find("<body")
            search_from = body_start if body_start != -1 else 0
            tags = list(IMG_RE.finditer(src, search_from))
            if not tags:
                continue

            first_tag_match = tags[0]
            tag = first_tag_match.group(0)
            if has_attr(tag, "fetchpriority") or "${" in tag:
                continue

            new_tag = re.sub(r"<img\b", '<img fetchpriority="high"', tag, count=1)
            new_src = src[:first_tag_match.start()] + new_tag + src[first_tag_match.end():]

            rel = os.path.relpath(fp, ROOT).replace("\\", "/")
            changed.append(rel)
            if not DRY_RUN:
                with open(fp, "w", encoding="utf-8", newline="") as fh:
                    fh.write(new_src)

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Pages updated: {len(changed)}")
    for r in changed[:15]:
        print(f"  {r}")
    if len(changed) > 15:
        print(f"  ... and {len(changed) - 15} more")


if __name__ == "__main__":
    main()
