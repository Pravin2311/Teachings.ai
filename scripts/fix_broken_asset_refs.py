"""
Fixes the remaining broken/mismatched asset references found by
audit_case_sensitivity.py and audit_broken_content_images.py:

1. Favicon/apple-touch-icon chaos: 9 different broken variants
   (assets/favicon.ico, assets/images/favicon.ico, /favicon.ico,
   icon-192x192.png, CDN-prefixed versions, etc.) across the site --
   none of those files exist. The real, working icons are
   assets/images/app_icon_192.png and app_icon_512.png (used correctly
   in manifest.json). Normalizes every variant to those two.

2. 16 pages loaded "assets/js/globalImageLoader.js" (no such directory)
   instead of the real "js/globalImageLoader.js".

3. Case-sensitivity bugs invisible on Windows but live 404s on GitHub
   Pages' case-sensitive hosting: canada.png/china.png/france.png/
   japan.png -> Canada.png/China.png/France.png/Japan.png.

4. phonic-words.html's default <audio> pointed at "audio/cat.mp3"
   (doesn't exist); the real file is assets/audio/animals/cat.mp3.

5. phonic-rhyming.html's "wrong" feedback sound pointed at
   math_feedback/wrong.mp3; the real file in that folder is
   incorrect.mp3 (correct.mp3's sibling).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
DRY_RUN = "--dry-run" in sys.argv

FAVICON_TAG_RE = re.compile(r'<link rel="icon"[^>]*>')
APPLE_TAG_RE = re.compile(r'<link rel="apple-touch-icon"[^>]*>')

REAL_ICON = "/assets/images/app_icon_192.png"
REAL_APPLE_ICON = "/assets/images/app_icon_512.png"

SIMPLE_REPLACEMENTS = {
    'src="assets/js/globalImageLoader.js"': 'src="js/globalImageLoader.js"',
    '/assets/images/flags/canada.png': '/assets/images/flags/Canada.png',
    '/assets/images/flags/china.png': '/assets/images/flags/China.png',
    '/assets/images/flags/france.png': '/assets/images/flags/France.png',
    '/assets/images/flags/japan.png': '/assets/images/flags/Japan.png',
    'src="audio/cat.mp3"': 'src="assets/audio/animals/cat.mp3"',
    'assets/audio/math_feedback/wrong.mp3': 'assets/audio/math_feedback/incorrect.mp3',
}


def fix_favicons(content):
    n = 0
    content, c1 = FAVICON_TAG_RE.subn(f'<link rel="icon" href="{REAL_ICON}" type="image/png">', content)
    n += c1
    content, c2 = APPLE_TAG_RE.subn(f'<link rel="apple-touch-icon" href="{REAL_APPLE_ICON}">', content)
    n += c2
    return content, n


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
            original = content
            total = 0

            content, n = fix_favicons(content)
            total += n

            for old, new in SIMPLE_REPLACEMENTS.items():
                if old in content:
                    total += content.count(old)
                    content = content.replace(old, new)

            if content != original:
                rel = os.path.relpath(fp, ROOT).replace("\\", "/")
                changed.append((rel, total))
                if not DRY_RUN:
                    with open(fp, "w", encoding="utf-8", newline="") as fh:
                        fh.write(content)

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Files changed: {len(changed)}")
    for rel, n in changed:
        print(f"  {rel}: {n} fix(es)")


if __name__ == "__main__":
    main()
