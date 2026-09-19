#!/usr/bin/env python3
"""Adds missing Open Graph and Twitter Card meta tags across the site.

For each page, only inserts the specific og:*/twitter:* tags that are
actually missing (many pages already have some but not all). Values are
derived from the page's own <title>, meta description, and canonical URL,
so no content is invented. Falls back to the site logo for og:image /
twitter:image when the page doesn't declare its own image.
Idempotent and safe to re-run.
"""
import glob
import re
import html as htmlmod
import sys

SKIP_DIRS = ("mockups/", ".git/", "node_modules/")
SKIP_FILES = {"furits-vegetables-sorting.html"}  # redirect stub, not real content
DEFAULT_IMAGE = "https://www.teachings.ai/assets/images/app_logo.png"

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'<meta\s+[^>]*name=["\']description["\'][^>]*content=(["\'])(.*?)\1', re.S | re.I)
CANONICAL_RE = re.compile(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=(["\'])(.*?)\1', re.S | re.I)
OG_IMAGE_URL_RE = re.compile(r'property=["\']og:image["\'][^>]*content=(["\'])(.*?)\1', re.S | re.I)


def has_tag(html_src, pattern):
    return re.search(pattern, html_src, re.I) is not None


def build_insert(html_src, title, desc, canonical):
    lines = []

    def og_present(prop):
        return has_tag(html_src, rf'property=["\']{re.escape(prop)}["\']')

    if not og_present("og:title"):
        lines.append(f'  <meta property="og:title" content="{title}">')
    if not og_present("og:description"):
        lines.append(f'  <meta property="og:description" content="{desc}">')
    if not og_present("og:type"):
        lines.append('  <meta property="og:type" content="website">')
    if not og_present("og:url") and canonical:
        lines.append(f'  <meta property="og:url" content="{canonical}">')
    if not og_present("og:site_name"):
        lines.append('  <meta property="og:site_name" content="Teachings.ai">')

    existing_image_m = OG_IMAGE_URL_RE.search(html_src)
    image_url = existing_image_m.group(2) if existing_image_m else DEFAULT_IMAGE
    if not og_present("og:image"):
        lines.append(f'  <meta property="og:image" content="{image_url}">')

    if not has_tag(html_src, r'name=["\']twitter:card["\']'):
        lines.append('  <meta name="twitter:card" content="summary_large_image">')
    if not has_tag(html_src, r'name=["\']twitter:title["\']'):
        lines.append(f'  <meta name="twitter:title" content="{title}">')
    if not has_tag(html_src, r'name=["\']twitter:description["\']'):
        lines.append(f'  <meta name="twitter:description" content="{desc}">')
    if not has_tag(html_src, r'name=["\']twitter:image["\']'):
        lines.append(f'  <meta name="twitter:image" content="{image_url}">')

    return lines


def process(fname, dry_run):
    src = open(fname, encoding="utf-8").read()

    tm = TITLE_RE.search(src)
    dm = DESC_RE.search(src)
    cm = CANONICAL_RE.search(src)
    if not tm or not dm:
        return "no-title-or-desc", None

    title = htmlmod.unescape(tm.group(1).strip()).replace('"', "&quot;")
    desc = htmlmod.unescape(dm.group(2).strip()).replace('"', "&quot;")
    canonical = cm.group(2).strip() if cm else None

    new_lines = build_insert(src, title, desc, canonical)
    if not new_lines:
        return "already-complete", None

    insert_block = "\n".join(new_lines) + "\n"

    # insert right after the meta description tag (fallback: after <title>)
    anchor = DESC_RE.search(src)
    if anchor:
        insert_pos = anchor.end()
        # move to end of line
        nl = src.find("\n", insert_pos)
        insert_pos = nl + 1 if nl != -1 else insert_pos
    else:
        anchor2 = TITLE_RE.search(src)
        insert_pos = anchor2.end()
        nl = src.find("\n", insert_pos)
        insert_pos = nl + 1 if nl != -1 else insert_pos

    new_src = src[:insert_pos] + insert_block + src[insert_pos:]

    if not dry_run:
        with open(fname, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_src)

    return "changed", len(new_lines)


def main():
    dry_run = "--dry-run" in sys.argv
    files = [f for f in glob.glob("**/*.html", recursive=True) if not f.startswith(SKIP_DIRS)]
    files = [f for f in files if f.replace("\\", "/") not in SKIP_FILES]
    files.sort()

    changed, complete, errors = 0, 0, 0
    for f in files:
        status, count = process(f, dry_run)
        if status == "changed":
            changed += 1
            print(f"[{'DRY' if dry_run else 'OK'}] {f}: +{count} tags")
        elif status == "already-complete":
            complete += 1
        else:
            errors += 1
            print(f"[SKIP:{status}] {f}")

    print(f"\nchanged={changed} already_complete={complete} errors={errors} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
