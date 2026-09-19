#!/usr/bin/env python3
"""Audits every <img> tag across the site for basic image SEO/performance
hygiene:
- missing or empty alt text
- missing width/height (causes layout shift / hurts CLS)
- missing loading="lazy" (except images likely above the fold, which we
  don't try to detect -- just report the raw count, judgment call is manual)
Read-only report, no modifications.
"""
import glob
import re

SKIP_DIRS = ("mockups/", ".git/", "node_modules/")
SKIP_FILES = {"furits-vegetables-sorting.html"}

IMG_RE = re.compile(r"<img\b[^>]*>", re.I)


def get_attr(tag, name):
    m = re.search(rf'{name}\s*=\s*"([^"]*)"', tag, re.I)
    if m:
        return m.group(1)
    m = re.search(rf"{name}\s*=\s*'([^']*)'", tag, re.I)
    if m:
        return m.group(1)
    return None


def main():
    files = [f for f in glob.glob("**/*.html", recursive=True) if not f.startswith(SKIP_DIRS)]
    files = [f for f in files if f.replace("\\", "/") not in SKIP_FILES]
    files.sort()

    total_imgs = 0
    missing_alt = []
    empty_alt = []
    missing_dims = []
    missing_lazy = []
    pages_with_imgs = 0

    for f in files:
        try:
            html = open(f, encoding="utf-8", errors="ignore").read()
        except Exception as e:
            print(f"READ ERROR {f}: {e}")
            continue

        imgs = IMG_RE.findall(html)
        if not imgs:
            continue
        pages_with_imgs += 1

        for tag in imgs:
            total_imgs += 1
            alt = get_attr(tag, "alt")
            if alt is None:
                missing_alt.append((f, tag[:100]))
            elif alt.strip() == "":
                empty_alt.append((f, tag[:100]))

            w = get_attr(tag, "width")
            h = get_attr(tag, "height")
            if not w or not h:
                missing_dims.append((f, tag[:100]))

            loading = get_attr(tag, "loading")
            if loading != "lazy":
                missing_lazy.append((f, tag[:100]))

    print("=" * 70)
    print(f"Total HTML pages scanned: {len(files)}")
    print(f"Pages containing <img> tags: {pages_with_imgs}")
    print(f"Total <img> tags found: {total_imgs}")
    print(f"Missing alt attribute entirely: {len(missing_alt)}")
    print(f"Empty alt=\"\" (decorative, may be OK): {len(empty_alt)}")
    print(f"Missing width or height: {len(missing_dims)}")
    print(f"Missing loading=\"lazy\": {len(missing_lazy)}")
    print("=" * 70)

    def dump(label, rows, limit=400):
        print(f"\n[{label}] ({len(rows)}):")
        for f, tag in rows[:limit]:
            print(f"  {f}: {tag}")
        if len(rows) > limit:
            print(f"  ... and {len(rows) - limit} more")

    dump("MISSING ALT", missing_alt)


if __name__ == "__main__":
    main()
