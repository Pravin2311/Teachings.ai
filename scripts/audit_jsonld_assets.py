"""
Found the assets/images/logo.png bug (5 pages, JSON-LD publisher.logo
field) by luck while fixing something else -- og:image/twitter:image and
<img src> are already covered by other audits, but nothing has
systematically checked every asset-shaped URL string INSIDE JSON-LD
blocks (logo, image, thumbnailUrl, or any other field). This does that:
parses every <script type="application/ld+json"> block as real JSON,
walks every string value, and checks any that looks like a local
teachings.ai asset URL against the real (case-exact) filesystem.
"""
import os
import re
import json
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}

SCRIPT_RE = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL | re.IGNORECASE
)
ASSET_URL_RE = re.compile(r'^https://(?:www\.)?teachings\.ai/(assets/[^\s"]+)$')

_real_files = set()
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
    for fn in filenames:
        rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/")
        _real_files.add(rel)


def walk_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_strings(v)


def main():
    broken = {}
    blocks_checked = 0
    urls_checked = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            rel_file = os.path.relpath(fp, ROOT).replace("\\", "/")
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            for m in SCRIPT_RE.finditer(content):
                blocks_checked += 1
                try:
                    data = json.loads(m.group(1))
                except json.JSONDecodeError:
                    continue
                for s in walk_strings(data):
                    am = ASSET_URL_RE.match(s.split("#")[0].split("?")[0])
                    if not am:
                        continue
                    urls_checked += 1
                    target = unquote(am.group(1))
                    if target not in _real_files:
                        broken.setdefault(target, []).append(rel_file)

    print(f"JSON-LD blocks checked: {blocks_checked}")
    print(f"Local asset URLs checked inside JSON-LD: {urls_checked}")
    print(f"Broken asset URLs found: {len(broken)}")
    print()
    for target, pages in sorted(broken.items()):
        print(f"  {target}  ({len(set(pages))} pages)")
        for p in sorted(set(pages))[:5]:
            print(f"    {p}")


if __name__ == "__main__":
    main()
