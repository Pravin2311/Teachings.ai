"""
audit_og_images.py only checks og:image/twitter:image. This checks every
<img src> in the actual page body -- a broken content image (not just a
broken social preview) directly hurts trust, time-on-page, and looks
broken to a parent or child using the page.

Resolves local paths, root-relative paths, and the jsDelivr CDN mirror of
this same repo (used site-wide for some assets). Skips JS template-
literal src values (${...}) and data: URIs, which can't be resolved
statically.
"""
import os
import re
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
CDN_PREFIX = "https://cdn.jsdelivr.net/gh/Pravin2311/Teachings.ai@main/"

IMG_SRC_RE = re.compile(r'<img\b[^>]*\bsrc="([^"]+)"', re.IGNORECASE)


def resolve(src, source_file):
    if "${" in src or src.startswith("data:"):
        return None  # dynamic / inline, can't check statically
    if src.startswith(CDN_PREFIX):
        rel = src[len(CDN_PREFIX):]
    elif src.startswith("http://") or src.startswith("https://"):
        return None  # external, out of scope
    elif src.startswith("/"):
        rel = src.lstrip("/")
    else:
        source_dir = os.path.dirname(source_file)
        rel = os.path.normpath(os.path.join(source_dir, src)).replace("\\", "/")
    return unquote(rel)


def main():
    broken = {}
    total_imgs = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            rel_file = os.path.relpath(fp, ROOT).replace("\\", "/")
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            for m in IMG_SRC_RE.finditer(content):
                total_imgs += 1
                src = m.group(1)
                target = resolve(src, rel_file)
                if target is None:
                    continue
                if not os.path.isfile(os.path.join(ROOT, target)):
                    broken.setdefault(target, []).append(rel_file)

    print(f"Total <img> tags scanned: {total_imgs}")
    print(f"Unique broken content-image targets: {len(broken)}")
    affected = len(set(f for fs in broken.values() for f in fs))
    print(f"Pages affected: {affected}")
    print()
    for target, pages in sorted(broken.items(), key=lambda kv: -len(kv[1])):
        print(f"{target}  ({len(pages)} refs)")
        for p in sorted(set(pages))[:4]:
            print(f"    {p}")


if __name__ == "__main__":
    main()
