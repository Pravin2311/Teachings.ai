"""
Fixes two duplicate-third-party-script bugs found by audit_performance.py:

1. AdSense loader duplication (~385 pages): the Google-provided ad-unit
   snippet (loader script + <ins> + push call) was pasted per ad slot,
   so the SAME adsbygoogle.js loader <script src> is fetched/executed
   multiple times on one page (once in <head>, again before each inline
   ad). Only the loader needs to load once; every <ins class="adsbygoogle">
   + its own push() call is still required and is left untouched.

2. Full Google Analytics + AdSense boilerplate duplicated wholesale in
   <head> (11 pages, all learn/colors/*.html): gtag('config', ...) fires
   twice per pageview, double-counting traffic in GA4 -- a real data
   integrity bug, not just a perf one.

Both are fixed the same way: keep the FIRST occurrence of each known
boilerplate script tag in the document, delete exact duplicates.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
DRY_RUN = "--dry-run" in sys.argv

ADSENSE_RE = re.compile(
    r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/?(?:adsbygoogle\.js)?\?client=ca-pub-7495143337429327"'
    r'\s*\n?\s*crossorigin="anonymous"\s*>\s*</script>\n?'
)
GA_LOADER_RE = re.compile(
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-XVYMNTZLQJ"></script>\n?'
)
GA_CONFIG_RE = re.compile(
    r'<script>\s*\n?\s*window\.dataLayer = window\.dataLayer \|\| \[\];\s*\n?'
    r'\s*function gtag\(\)\{\s*dataLayer\.push\(arguments\);?\s*\}\s*\n?'
    r'\s*gtag\(\'js\', new Date\(\)\);\s*\n?'
    r'\s*gtag\(\'config\', \'G-XVYMNTZLQJ\'\);\s*\n?'
    r'\s*</script>\n?'
)
def dedupe(content, pattern):
    matches = list(pattern.finditer(content))
    if len(matches) <= 1:
        return content, 0
    removed = 0
    out = content[:matches[0].end()]
    last_end = matches[0].end()
    for m in matches[1:]:
        out += content[last_end:m.start()]
        removed += 1
        last_end = m.end()
    out += content[last_end:]
    return out, removed


def main():
    total_files = 0
    total_adsense_removed = 0
    total_ga_loader_removed = 0
    total_ga_config_removed = 0
    changed_files = []

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            original = content

            content, n1 = dedupe(content, ADSENSE_RE)
            content, n2 = dedupe(content, GA_LOADER_RE)
            content, n3 = dedupe(content, GA_CONFIG_RE)

            if n1 or n2 or n3:
                # clean up now-orphaned boilerplate comments left with nothing after them
                # (only when a comment is immediately followed by another identical comment,
                # meaning the block it introduced was just deleted)
                content = re.sub(r'(<!--\s*Google Analytics[^>]*-->\s*\n)(?=\s*<!--\s*Google Analytics)', '', content)
                content = re.sub(r'(<!--\s*Google AdSense[^>]*-->\s*\n)(?=\s*<!--\s*Google AdSense)', '', content)
                content = re.sub(r'<!--\s*Google Analytics[^>]*-->\s*\n(?=\s*<!--\s*Google AdSense)', '', content)

            if content != original:
                total_files += 1
                total_adsense_removed += n1
                total_ga_loader_removed += n2
                total_ga_config_removed += n3
                rel = os.path.relpath(fp, ROOT).replace("\\", "/")
                changed_files.append((rel, n1, n2, n3))
                if not DRY_RUN:
                    with open(fp, "w", encoding="utf-8", newline="") as fh:
                        fh.write(content)

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Files changed: {total_files}")
    print(f"AdSense loader duplicates removed: {total_adsense_removed}")
    print(f"GA loader duplicates removed: {total_ga_loader_removed}")
    print(f"GA config-block duplicates removed: {total_ga_config_removed}")
    print()
    for rel, n1, n2, n3 in changed_files[:20]:
        print(f"  {rel}: adsense-{n1} ga_loader-{n2} ga_config-{n3}")
    if len(changed_files) > 20:
        print(f"  ... and {len(changed_files) - 20} more")


if __name__ == "__main__":
    main()
