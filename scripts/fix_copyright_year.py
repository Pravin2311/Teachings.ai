"""
52 pages' footers still say "© 2025 Teachings.AI" even though the site's
own content (datePublished/lastmod fields) is dated well into 2026 -- a
stale copyright year is a small but real staleness/trust signal. Updates
to "© 2025-2026 Teachings.AI" (keeps the real origin year, adds current).
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
DRY_RUN = "--dry-run" in sys.argv


def main():
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            if "© 2025" not in content:
                continue
            new_content = content.replace("© 2025", "© 2025-2026")
            rel = os.path.relpath(fp, ROOT).replace("\\", "/")
            changed.append(rel)
            if not DRY_RUN:
                with open(fp, "w", encoding="utf-8", newline="") as fh:
                    fh.write(new_content)

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Pages updated: {len(changed)}")
    for f in changed[:10]:
        print(f"  {f}")
    if len(changed) > 10:
        print(f"  ... and {len(changed) - 10} more")


if __name__ == "__main__":
    main()
