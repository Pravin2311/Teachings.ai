"""
The shared Organization JSON-LD entity (@id .../#organization) used across
~59 pages lists sameAs for Twitter, Facebook, and LinkedIn only -- but the
site's own footers link real, live Instagram and YouTube accounts too
(instagram.com/teachingsai, youtube.com/@teachingsai) that are missing from
the entity graph. Adds those two to every existing sameAs list so Google's
entity resolution has the complete set of verified profiles.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", ".git", "node_modules"}
DRY_RUN = "--dry-run" in sys.argv

PATTERN = re.compile(
    r'("sameAs":\s*\[\s*\n)'
    r'([ \t]*)"https://twitter\.com/TeachingsAI",\s*\n'
    r'[ \t]*"https://www\.facebook\.com/TeachingsAI",\s*\n'
    r'[ \t]*"https://www\.linkedin\.com/company/teachingsai"\s*\n'
    r'([ \t]*)\]'
)


def replacement(m):
    head, indent, close_indent = m.group(1), m.group(2), m.group(3)
    lines = [
        f'{indent}"https://twitter.com/TeachingsAI",',
        f'{indent}"https://www.facebook.com/TeachingsAI",',
        f'{indent}"https://www.instagram.com/teachingsai",',
        f'{indent}"https://www.youtube.com/@teachingsai",',
        f'{indent}"https://www.linkedin.com/company/teachingsai"',
    ]
    return head + "\n".join(lines) + "\n" + close_indent + "]"


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
            new_content, n = PATTERN.subn(replacement, content)
            if n:
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
