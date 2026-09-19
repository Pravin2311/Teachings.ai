#!/usr/bin/env python3
"""Audits every HTML page for indexing-blocking and basic technical SEO issues:
- noindex in robots meta (would block indexing entirely)
- missing canonical link
- canonical pointing to a different domain / malformed
- missing viewport meta
- missing og:title / og:description / og:image
- missing twitter:card
Read-only report, no modifications.
"""
import glob
import re

SKIP_DIRS = ("mockups/", ".git/", "node_modules/")


def main():
    files = [f for f in glob.glob("**/*.html", recursive=True) if not f.startswith(SKIP_DIRS)]
    files.sort()

    noindex = []
    missing_canonical = []
    bad_canonical = []
    missing_viewport = []
    missing_og = []
    missing_twitter = []

    for f in files:
        try:
            html = open(f, encoding="utf-8", errors="ignore").read()
        except Exception as e:
            print(f"READ ERROR {f}: {e}")
            continue

        if re.search(r'<meta\s+[^>]*name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', html, re.I):
            noindex.append(f)

        m = re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']', html, re.I)
        if not m:
            missing_canonical.append(f)
        else:
            href = m.group(1)
            if "teachings.ai" not in href.lower():
                bad_canonical.append((f, href))

        if not re.search(r'<meta\s+[^>]*name=["\']viewport["\']', html, re.I):
            missing_viewport.append(f)

        has_og_title = re.search(r'property=["\']og:title["\']', html, re.I)
        has_og_desc = re.search(r'property=["\']og:description["\']', html, re.I)
        has_og_image = re.search(r'property=["\']og:image["\']', html, re.I)
        if not (has_og_title and has_og_desc and has_og_image):
            missing_og.append(f)

        if not re.search(r'name=["\']twitter:card["\']', html, re.I):
            missing_twitter.append(f)

    print("=" * 70)
    print(f"Total HTML pages scanned: {len(files)}")
    print(f"noindex found:            {len(noindex)}")
    print(f"Missing canonical:        {len(missing_canonical)}")
    print(f"Bad/off-domain canonical: {len(bad_canonical)}")
    print(f"Missing viewport meta:    {len(missing_viewport)}")
    print(f"Missing OG tags (title/desc/image): {len(missing_og)}")
    print(f"Missing twitter:card:     {len(missing_twitter)}")
    print("=" * 70)

    def dump(label, rows):
        print(f"\n[{label}] ({len(rows)}):")
        for r in rows:
            print(f"  {r}")

    dump("NOINDEX", noindex)
    dump("MISSING CANONICAL", missing_canonical)
    print(f"\n[BAD CANONICAL] ({len(bad_canonical)}):")
    for f, href in bad_canonical:
        print(f"  {f}: {href}")
    dump("MISSING VIEWPORT", missing_viewport)
    dump("MISSING OG TAGS", missing_og)
    dump("MISSING TWITTER CARD", missing_twitter)


if __name__ == "__main__":
    main()
