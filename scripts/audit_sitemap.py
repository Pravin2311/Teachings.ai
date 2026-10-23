"""Checks that every real, live, indexable HTML page is listed in
sitemap.xml, that every sitemap URL resolves to a real file, and that no
noindex page is listed (a sitemap should only contain pages we want
indexed)."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
# indexable pages deliberately left out of the sitemap (not search landing pages)
NOT_IN_SITEMAP = {"feedback.html"}


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


def is_noindex(path):
    with open(os.path.join(ROOT, path), encoding="utf-8", errors="ignore") as fh:
        content = fh.read()
    return re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', content, re.I) is not None


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

    missing = sorted(f for f in files if f not in sm_paths and f not in NOT_IN_SITEMAP and not is_redirect_stub(f) and not is_noindex(f))
    extra = sorted(u for u in sm_paths if u not in files)
    noindex_listed = sorted(u for u in sm_paths if u in files and is_noindex(u))

    print(f"Real HTML files: {len(files)}")
    print(f"Sitemap URLs: {len(sm_paths)}")
    print(f"Live pages missing from sitemap: {len(missing)}")
    for m in missing:
        print(f"  {m}")
    print(f"Sitemap URLs pointing at nonexistent files: {len(extra)}")
    for e in extra:
        print(f"  {e}")
    print(f"Noindex pages listed in sitemap: {len(noindex_listed)}")
    for n in noindex_listed:
        print(f"  {n}")


if __name__ == "__main__":
    main()
