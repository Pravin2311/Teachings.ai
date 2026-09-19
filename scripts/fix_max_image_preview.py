"""
Google's actual default for max-image-preview (when no robots directive
specifies it) is "standard" -- a small thumbnail -- not "large". Since
this site's whole value proposition is visual (game screenshots, colorful
illustrations), missing this directive caps search-result and Google
Discover thumbnail size sitewide, directly hurting CTR.

Adds max-image-preview:large to every page's robots directive: appends
it to an existing <meta name="robots" content="..."> if present, or
inserts a new one (right after the viewport meta) if not. 0 pages have
noindex sitewide (verified via audit_technical_seo.py), so this is a
pure CTR/Discover-eligibility upgrade, not a crawling-behavior change.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", ".git", "node_modules"}
DRY_RUN = "--dry-run" in sys.argv

ROBOTS_RE = re.compile(r'(<meta name="robots" content=")([^"]*)("\s*/?>)')
VIEWPORT_RE = re.compile(r'[ \t]*<meta name="viewport"[^>]*/?>\s*\n?')


def main():
    updated_existing = 0
    added_new = 0
    skipped_redirect_stub = 0
    changed = []

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()

            if "max-image-preview" in content:
                continue

            m = ROBOTS_RE.search(content)
            if m:
                if "noindex" in m.group(2):
                    continue
                new_value = m.group(2).rstrip()
                new_value = new_value + ", max-image-preview:large"
                new_content = content[:m.start()] + m.group(1) + new_value + m.group(3) + content[m.end():]
                updated_existing += 1
            else:
                anchor = VIEWPORT_RE.search(content)
                if not anchor:
                    skipped_redirect_stub += 1
                    continue
                indent_match = re.match(r'[ \t]*', anchor.group(0))
                indent = indent_match.group(0) if indent_match else "  "
                insertion = f'{indent}<meta name="robots" content="index, follow, max-image-preview:large">\n'
                new_content = content[:anchor.end()] + insertion + content[anchor.end():]
                added_new += 1

            rel = os.path.relpath(fp, ROOT).replace("\\", "/")
            changed.append(rel)
            if not DRY_RUN:
                with open(fp, "w", encoding="utf-8", newline="") as fh:
                    fh.write(new_content)

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Pages changed: {len(changed)}")
    print(f"  Appended to existing robots tag: {updated_existing}")
    print(f"  New robots tag added: {added_new}")
    print(f"  Skipped (no viewport anchor, likely redirect stub): {skipped_redirect_stub}")
    for f in changed[:10]:
        print(f"  {f}")
    if len(changed) > 10:
        print(f"  ... and {len(changed) - 10} more")


if __name__ == "__main__":
    main()
