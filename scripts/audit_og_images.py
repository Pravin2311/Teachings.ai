"""
Checks every og:image / twitter:image URL sitewide actually resolves to a
real local file. A broken preview image means Google/social platforms
show no thumbnail at all for that page -- silently defeating any
max-image-preview / Discover-eligibility work.
"""
import os
import re
from collections import defaultdict
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}

IMG_META_RE = re.compile(
    r'<meta\s+(?:property|name)="(?:og:image|twitter:image)"\s+content="([^"]+)"',
    re.IGNORECASE,
)
DOMAIN_RE = re.compile(r'^https?://(www\.)?teachings\.ai', re.IGNORECASE)


def all_html_files():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html"):
                files.append(os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/"))
    return sorted(files)


def resolve(url):
    if not DOMAIN_RE.match(url):
        return None
    path = DOMAIN_RE.sub("", url).lstrip("/")
    return unquote(path)


def main():
    files = all_html_files()
    broken = defaultdict(list)
    checked_cache = {}

    for f in files:
        with open(os.path.join(ROOT, f), "r", encoding="utf-8", errors="ignore") as fh:
            content = fh.read()
        for m in IMG_META_RE.finditer(content):
            url = m.group(1)
            local_path = resolve(url)
            if local_path is None:
                continue
            if local_path not in checked_cache:
                checked_cache[local_path] = os.path.isfile(os.path.join(ROOT, local_path))
            if not checked_cache[local_path]:
                broken[local_path].append(f)

    print(f"Total pages scanned: {len(files)}")
    print(f"Unique broken og:image/twitter:image targets: {len(broken)}")
    total_pages_affected = len(set(f for fs in broken.values() for f in fs))
    print(f"Pages affected: {total_pages_affected}")
    print()
    for target, pages in sorted(broken.items(), key=lambda kv: -len(kv[1])):
        print(f"{target}  ({len(pages)} pages)")
        for p in pages[:3]:
            print(f"    {p}")
        if len(pages) > 3:
            print(f"    ... and {len(pages) - 3} more")


if __name__ == "__main__":
    main()
