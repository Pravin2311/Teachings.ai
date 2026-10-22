"""
Removes loading="lazy" from each page's hero/LCP image -- the <img> that
fix_hero_fetchpriority.py marked fetchpriority="high". The two attributes
contradict each other: a lazy image isn't requested until layout puts it
in the viewport, so the browser can't start fetching the page's largest
element early, which delays LCP. Every other image keeps loading="lazy".

Usage:
  python scripts/fix_hero_not_lazy.py [--dry-run] [--exclude REGEX]

--exclude skips pages whose repo-relative path matches REGEX (e.g. pages
inside a running SEO experiment that shouldn't change yet).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", "seo", ".git", "node_modules"}
DRY_RUN = "--dry-run" in sys.argv
EXCLUDE = re.compile(sys.argv[sys.argv.index("--exclude") + 1]) if "--exclude" in sys.argv else None

HERO_RE = re.compile(r'<img\b[^>]*\bfetchpriority="high"[^>]*>', re.I)
LAZY_RE = re.compile(r'\s+loading=["\']lazy["\']', re.I)


def main():
    changed, skipped = [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, ROOT).replace("\\", "/")
            with open(fp, "r", encoding="utf-8", errors="ignore", newline="") as fh:
                src = fh.read()

            m = HERO_RE.search(src)
            if not m or not LAZY_RE.search(m.group(0)):
                continue
            if EXCLUDE and EXCLUDE.search(rel):
                skipped.append(rel)
                continue

            new_tag = LAZY_RE.sub("", m.group(0), count=1)
            new_src = src[:m.start()] + new_tag + src[m.end():]
            changed.append(rel)
            if not DRY_RUN:
                with open(fp, "w", encoding="utf-8", newline="") as fh:
                    fh.write(new_src)

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Pages updated: {len(changed)}")
    for r in changed[:15]:
        print(f"  {r}")
    if len(changed) > 15:
        print(f"  ... and {len(changed) - 15} more")
    if skipped:
        print(f"Skipped by --exclude: {len(skipped)}")


if __name__ == "__main__":
    main()
