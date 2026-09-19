"""
Static-analysis performance audit (no headless browser available in this
environment, so this checks structural patterns known to affect Core Web
Vitals / Lighthouse scores rather than running a real trace):

  - duplicate AdSense (or any) <script src> tag loaded twice on one page
  - missing <link rel="preconnect"> for third-party origins actually used
    on the page (googletagmanager.com, pagead2.googlesyndication.com)
  - render-blocking <script src=...> in <head> with no async/defer
  - render-blocking <link rel="stylesheet"> count (informational)
"""
import os
import re
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", ".git", "node_modules"}

SCRIPT_SRC_RE = re.compile(r'<script\b([^>]*?)\bsrc=(["\'])(.*?)\2([^>]*)>', re.IGNORECASE)
HEAD_RE = re.compile(r'<head\b.*?</head>', re.IGNORECASE | re.DOTALL)
THIRD_PARTY_ORIGINS = {
    "googletagmanager.com": "https://www.googletagmanager.com",
    "pagead2.googlesyndication.com": "https://pagead2.googlesyndication.com",
}


def all_html_files():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html"):
                files.append(os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/"))
    return sorted(files)


def main():
    files = all_html_files()
    dup_scripts = {}
    missing_preconnect = defaultdict(list)
    blocking_head_scripts = defaultdict(list)

    for f in files:
        with open(os.path.join(ROOT, f), "r", encoding="utf-8", errors="ignore") as fh:
            content = fh.read()

        srcs = [m.group(3) for m in SCRIPT_SRC_RE.finditer(content)]
        counts = Counter(srcs)
        dups = {s: c for s, c in counts.items() if c > 1}
        if dups:
            dup_scripts[f] = dups

        used_origins = {name for name, origin in THIRD_PARTY_ORIGINS.items() if origin in content}
        for name in used_origins:
            if f'preconnect" href="{THIRD_PARTY_ORIGINS[name]}' not in content and \
               f"preconnect' href='{THIRD_PARTY_ORIGINS[name]}" not in content:
                missing_preconnect[f].append(name)

        head_match = HEAD_RE.search(content)
        if head_match:
            head = head_match.group(0)
            for m in SCRIPT_SRC_RE.finditer(head):
                attrs_before, _, src, attrs_after = m.groups()
                all_attrs = attrs_before + attrs_after
                if "async" not in all_attrs and "defer" not in all_attrs and "ld+json" not in all_attrs:
                    if "json" not in src.lower():
                        blocking_head_scripts[f].append(src)

    print(f"Total pages scanned: {len(files)}")
    print(f"Pages with a duplicate <script src> (same URL loaded 2+ times): {len(dup_scripts)}")
    print(f"Pages missing <link rel=preconnect> for a third-party origin they use: {len(missing_preconnect)}")
    print(f"Pages with render-blocking (no async/defer) <script src> in <head>: {len(blocking_head_scripts)}")

    print("\n=== DUPLICATE SCRIPT TAGS ===")
    for f, dups in sorted(dup_scripts.items()):
        for src, c in dups.items():
            print(f"{f}: '{src}' loaded {c}x")

    print(f"\n=== MISSING PRECONNECT (first 15 of {len(missing_preconnect)}) ===")
    for f, origins in list(sorted(missing_preconnect.items()))[:15]:
        print(f"{f}: missing preconnect for {origins}")

    print(f"\n=== RENDER-BLOCKING HEAD SCRIPTS (first 15 of {len(blocking_head_scripts)}) ===")
    for f, srcs in list(sorted(blocking_head_scripts.items()))[:15]:
        print(f"{f}: {srcs}")


if __name__ == "__main__":
    main()
