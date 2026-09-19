"""Checks that every real, live HTML page is listed in sitemap.xml, and
that every sitemap URL resolves to a real file -- both directions matter
for the "get every page indexed" goal."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}


def all_html_files():
    files = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html"):
                files.add(os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/"))
    return files


def is_redirect_stub(path):
    with open(os.path.join(ROOT, path), encoding="utf-8", errors="ignore") as fh:
        head = fh.read(500)
    return "http-equiv=\"refresh\"" in head


def main():
    files = all_html_files()
    with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as fh:
        sm = fh.read()
    urls = re.findall(r"<loc>https://www\.teachings\.ai/([^<]*)</loc>", sm)
    sm_paths = set()
    for u in urls:
        if u == "" or u.endswith("/"):
            u += "index.html"
        sm_paths.add(u)

    missing = sorted(f for f in files if f not in sm_paths and not is_redirect_stub(f))
    extra = sorted(u for u in sm_paths if u not in files)

    print(f"Real HTML files: {len(files)}")
    print(f"Sitemap URLs: {len(sm_paths)}")
    print(f"Live pages missing from sitemap: {len(missing)}")
    for m in missing:
        print(f"  {m}")
    print(f"Sitemap URLs pointing at nonexistent files: {len(extra)}")
    for e in extra:
        print(f"  {e}")


if __name__ == "__main__":
    main()
