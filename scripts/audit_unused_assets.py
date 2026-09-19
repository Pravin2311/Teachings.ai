"""
Checks every file under css/ and js/ for whether any live HTML page
actually references it. An unreferenced file is dead weight in the
repo (not a live-site bug -- browsers never fetch it -- but worth
knowing about for repo hygiene / catching abandoned duplicates like
"grammar copy.css").
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}

REF_RE = re.compile(r'(?:src|href)="([^"]+)"')


def all_html_text():
    text = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html"):
                with open(os.path.join(dirpath, fn), "r", encoding="utf-8", errors="ignore") as fh:
                    text.append(fh.read())
    return "\n".join(text)


def main():
    combined = all_html_text()
    for folder in ("css", "js"):
        base = os.path.join(ROOT, folder)
        if not os.path.isdir(base):
            continue
        print(f"=== {folder}/ ===")
        for fn in sorted(os.listdir(base)):
            fp = os.path.join(base, fn)
            if not os.path.isfile(fp):
                continue
            if fn not in combined:
                size = os.path.getsize(fp)
                print(f"  UNREFERENCED: {folder}/{fn}  ({size} bytes)")


if __name__ == "__main__":
    main()
