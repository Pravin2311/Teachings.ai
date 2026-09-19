"""
Audit internal linking density across the site.

Builds a full internal link graph (every <a href> that resolves to a local
.html file) and reports:
  - orphan pages: 0 inbound internal links (not linked from ANY other page)
  - thin pages: fewer than MIN_OUTBOUND outbound internal links
  - hub concentration: how link equity is distributed

Resolution handles: relative paths, root-relative "/..." paths, links with
trailing "/index.html" vs directory form, "#fragment" and "?query" stripping,
and absolute teachings.ai URLs.
"""
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", ".git", "node_modules"}
MIN_OUTBOUND = 3

HREF_RE = re.compile(r'href=(["\'])(.*?)\1', re.IGNORECASE)
DOMAIN_RE = re.compile(r'^https?://(www\.)?teachings\.ai', re.IGNORECASE)


def all_html_files():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html"):
                files.append(os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/"))
    return sorted(files)


def normalize(path):
    """Normalize a repo-relative html path: strip trailing /index.html duplication issues, lowercase drive-agnostic."""
    path = path.replace("\\", "/")
    if path == "" or path == "/":
        path = "index.html"
    path = path.lstrip("/")
    return path


def resolve_href(href, source_file):
    href = href.strip()
    if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:") \
       or href.startswith("javascript:") or href.startswith("data:"):
        return None
    if href.startswith("http://") or href.startswith("https://"):
        if not DOMAIN_RE.match(href):
            return None
        href = DOMAIN_RE.sub("", href)
        if not href.startswith("/"):
            href = "/" + href
    # strip query/fragment
    href = href.split("#")[0].split("?")[0]
    if not href:
        return None
    if href.startswith("/"):
        target = href.lstrip("/")
    else:
        source_dir = os.path.dirname(source_file)
        target = os.path.normpath(os.path.join(source_dir, href)).replace("\\", "/")
    if target == "" or target.endswith("/"):
        target = target + "index.html"
    if not target.endswith(".html"):
        return None
    return normalize(target)


def main():
    files = all_html_files()
    file_set = set(files)
    outbound = defaultdict(set)
    inbound = defaultdict(set)
    broken_links = defaultdict(list)

    for f in files:
        try:
            with open(os.path.join(ROOT, f), "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
        except Exception as e:
            print(f"ERROR reading {f}: {e}")
            continue
        for m in HREF_RE.finditer(content):
            href = m.group(2)
            target = resolve_href(href, f)
            if target is None:
                continue
            if target == f:
                continue
            if target not in file_set:
                broken_links[f].append(target)
                continue
            outbound[f].add(target)
            inbound[target].add(f)

    orphans = sorted(f for f in files if len(inbound[f]) == 0)
    thin = sorted(files, key=lambda f: len(outbound[f]))
    thin = [f for f in thin if len(outbound[f]) < MIN_OUTBOUND]

    print(f"Total HTML pages: {len(files)}")
    print(f"Pages with 0 inbound internal links (orphans): {len(orphans)}")
    print(f"Pages with < {MIN_OUTBOUND} outbound internal links: {len(thin)}")
    total_broken = sum(len(v) for v in broken_links.values())
    print(f"Broken internal links (href resolves to no file): {total_broken} across {len(broken_links)} pages")

    print("\n=== ORPHAN PAGES (0 inbound) ===")
    for f in orphans:
        print(f)

    print(f"\n=== THIN PAGES (<{MIN_OUTBOUND} outbound internal links) ===")
    for f in thin:
        print(f"{f}  ({len(outbound[f])} outbound)")

    print("\n=== BROKEN INTERNAL LINKS (top 40 pages by count) ===")
    for f, targets in sorted(broken_links.items(), key=lambda kv: -len(kv[1]))[:40]:
        uniq = sorted(set(targets))
        print(f"{f}: {len(targets)} broken -> {uniq[:5]}{'...' if len(uniq) > 5 else ''}")

    # inbound distribution summary
    counts = sorted((len(inbound[f]) for f in files), reverse=True)
    if counts:
        print(f"\nInbound link count -- max: {counts[0]}, median: {counts[len(counts)//2]}, "
              f"pages with exactly 1 inbound: {sum(1 for c in counts if c == 1)}")

    if "--save" in sys.argv:
        import json
        out = {
            "orphans": orphans,
            "thin": {f: len(outbound[f]) for f in thin},
            "broken": {f: sorted(set(v)) for f, v in broken_links.items()},
            "inbound_counts": {f: len(inbound[f]) for f in files},
            "outbound_counts": {f: len(outbound[f]) for f in files},
        }
        with open(os.path.join(ROOT, "scripts", "_link_graph.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1)
        print("\nSaved graph data to scripts/_link_graph.json")


if __name__ == "__main__":
    main()
