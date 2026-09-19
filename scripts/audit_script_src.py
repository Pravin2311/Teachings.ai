"""Checks every <script src="..."> reference resolves to a real, case-exact
local file -- the same class of bug already fixed for CSS/images, but
never checked comprehensively for JS."""
import os
import re
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
SCRIPT_RE = re.compile(r'<script\b[^>]*\bsrc="([^"]+)"', re.IGNORECASE)

_real_files = set()
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
    for fn in filenames:
        rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/")
        _real_files.add(rel)


def main():
    broken = {}
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
                src = m.group(1)
                if src.startswith("http") or "${" in src:
                    continue
                if src.startswith("/"):
                    target = src.lstrip("/")
                else:
                    source_dir = os.path.dirname(rel_file)
                    target = os.path.normpath(os.path.join(source_dir, src)).replace("\\", "/")
                target = unquote(target)
                if target not in _real_files:
                    broken.setdefault(target, []).append(rel_file)

    print(f"Broken <script src> refs: {len(broken)}")
    for t, pages in broken.items():
        print(f"  {t}  ({len(set(pages))} pages)")
        for p in sorted(set(pages))[:5]:
            print(f"    {p}")


if __name__ == "__main__":
    main()
