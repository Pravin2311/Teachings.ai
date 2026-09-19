"""
Adds <link rel="preconnect"> for third-party origins the page actually
loads render-relevant scripts from (Google Analytics, AdSense), so the
browser can start DNS+TCP+TLS for them immediately instead of only after
parsing reaches the <script> tag. Cheap, safe, real Core Web Vitals win.

Inserted right after the viewport meta tag (present on effectively every
page); falls back to right after <meta charset> if no viewport tag.
Skips a page/origin pair if that preconnect is already present.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
DRY_RUN = "--dry-run" in sys.argv

ORIGINS = [
    ("https://www.googletagmanager.com", "googletagmanager.com/gtag/js", False),
    ("https://pagead2.googlesyndication.com", "pagead2.googlesyndication.com", True),
]

VIEWPORT_RE = re.compile(r'[ \t]*<meta name="viewport"[^>]*/?>\s*\n?')
CHARSET_RE = re.compile(r'[ \t]*<meta charset="?UTF-8"?\s*/?>\s*\n?', re.IGNORECASE)


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

            needed = []
            for origin, marker, needs_crossorigin in ORIGINS:
                if marker not in content:
                    continue
                if f'preconnect" href="{origin}' in content:
                    continue
                needed.append((origin, needs_crossorigin))

            if not needed:
                continue

            anchor = VIEWPORT_RE.search(content)
            if not anchor:
                anchor = CHARSET_RE.search(content)
            if not anchor:
                continue

            indent_match = re.match(r'[ \t]*', anchor.group(0))
            indent = indent_match.group(0) if indent_match else "  "
            lines = []
            for origin, needs_crossorigin in needed:
                attr = " crossorigin" if needs_crossorigin else ""
                lines.append(f'{indent}<link rel="preconnect" href="{origin}"{attr}>\n')
            insertion = "".join(lines)

            new_content = content[:anchor.end()] + insertion + content[anchor.end():]
            rel = os.path.relpath(fp, ROOT).replace("\\", "/")
            changed.append((rel, len(needed)))
            if not DRY_RUN:
                with open(fp, "w", encoding="utf-8", newline="") as fh:
                    fh.write(new_content)

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Pages updated: {len(changed)}")
    total = sum(n for _, n in changed)
    print(f"Preconnect tags added: {total}")
    for rel, n in changed[:10]:
        print(f"  {rel}: +{n}")
    if len(changed) > 10:
        print(f"  ... and {len(changed) - 10} more")


if __name__ == "__main__":
    main()
