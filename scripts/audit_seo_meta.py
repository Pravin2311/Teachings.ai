#!/usr/bin/env python3
"""Audits every HTML page's <title> and meta description for CTR-relevant SEO issues:
- missing title / meta description
- title length outside 50-60 chars (Google's typical SERP display window)
- description length outside 140-155 chars
- duplicate titles / descriptions across pages (dilutes ranking + confuses CTR data)
- generic/boilerplate titles or descriptions
Read-only report, no modifications.
"""
import glob
import re
import html

SKIP_DIRS = ("mockups/", "templates/", ".git/", "node_modules/")

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

GENERIC_TITLE_PATTERNS = [
    re.compile(r"^teachings\.ai$", re.I),
    re.compile(r"^home\s*[-|]?\s*teachings\.ai$", re.I),
    re.compile(r"^untitled", re.I),
]


def extract_title(html_src):
    m = re.search(r"<title[^>]*>(.*?)</title>", html_src, re.S | re.I)
    if not m:
        return None
    return html.unescape(re.sub(r"\s+", " ", m.group(1)).strip())


def extract_description(html_src):
    # match either attribute order: name then content, or content then name
    # use a backreference so the capture stops at the SAME quote char that opened
    # it (content attributes routinely contain apostrophes, e.g. "What's typical...")
    m = re.search(
        r'<meta\s+[^>]*name=["\']description["\'][^>]*content=(["\'])(.*?)\1',
        html_src, re.S | re.I,
    )
    if not m:
        m = re.search(
            r'<meta\s+[^>]*content=(["\'])(.*?)\1[^>]*name=["\']description["\']',
            html_src, re.S | re.I,
        )
    if not m:
        return None
    return html.unescape(re.sub(r"\s+", " ", m.group(2)).strip())


def main():
    files = [f for f in glob.glob("**/*.html", recursive=True) if not f.replace("\\", "/").startswith(SKIP_DIRS)]
    files.sort()

    total = 0
    missing_title = []
    missing_desc = []
    title_too_short = []
    title_too_long = []
    desc_too_short = []
    desc_too_long = []
    generic_title = []
    titles_seen = {}
    descs_seen = {}

    for f in files:
        try:
            src = open(f, encoding="utf-8", errors="ignore").read()
        except Exception as e:
            print(f"READ ERROR {f}: {e}")
            continue
        total += 1

        title = extract_title(src)
        desc = extract_description(src)

        if not title:
            missing_title.append(f)
        else:
            n = len(title)
            if n < TITLE_MIN:
                title_too_short.append((f, n, title))
            elif n > TITLE_MAX:
                title_too_long.append((f, n, title))
            titles_seen.setdefault(title.lower(), []).append(f)
            if any(p.search(title) for p in GENERIC_TITLE_PATTERNS):
                generic_title.append((f, title))

        if not desc:
            missing_desc.append(f)
        else:
            n = len(desc)
            if n < DESC_MIN:
                desc_too_short.append((f, n, desc))
            elif n > DESC_MAX:
                desc_too_long.append((f, n, desc))
            descs_seen.setdefault(desc.lower(), []).append(f)

    dup_titles = {t: fl for t, fl in titles_seen.items() if len(fl) > 1}
    dup_descs = {d: fl for d, fl in descs_seen.items() if len(fl) > 1}

    print("=" * 70)
    print(f"Total HTML pages scanned: {total}")
    print(f"Missing <title>: {len(missing_title)}")
    print(f"Missing meta description: {len(missing_desc)}")
    print(f"Title length target: {TITLE_MIN}-{TITLE_MAX} chars")
    print(f"  Too short: {len(title_too_short)}   Too long: {len(title_too_long)}")
    print(f"Description length target: {DESC_MIN}-{DESC_MAX} chars")
    print(f"  Too short: {len(desc_too_short)}   Too long: {len(desc_too_long)}")
    print(f"Duplicate titles (groups): {len(dup_titles)}  (pages involved: {sum(len(v) for v in dup_titles.values())})")
    print(f"Duplicate descriptions (groups): {len(dup_descs)}  (pages involved: {sum(len(v) for v in dup_descs.values())})")
    print(f"Generic/boilerplate titles: {len(generic_title)}")
    print("=" * 70)

    def dump(label, rows, show_text=True):
        print(f"\n[{label}] ({len(rows)}):")
        for row in rows:
            if show_text:
                f, n, t = row
                print(f"  {f}: {n} chars -> {t!r}")
            else:
                f, t = row
                print(f"  {f}: {t!r}")

    print("\n[MISSING TITLE]:")
    for f in missing_title:
        print(" ", f)

    print("\n[MISSING DESCRIPTION]:")
    for f in missing_desc:
        print(" ", f)

    dump("TITLE TOO SHORT", title_too_short)
    dump("TITLE TOO LONG", title_too_long)
    dump("DESCRIPTION TOO SHORT", desc_too_short)
    dump("DESCRIPTION TOO LONG", desc_too_long)
    dump("GENERIC TITLE", generic_title, show_text=False)

    print(f"\n[DUPLICATE TITLES] ({len(dup_titles)} groups):")
    for t, fl in sorted(dup_titles.items(), key=lambda kv: -len(kv[1])):
        print(f"  {t!r} ({len(fl)} pages):")
        for f in fl:
            print(f"    {f}")

    print(f"\n[DUPLICATE DESCRIPTIONS] ({len(dup_descs)} groups):")
    for d, fl in sorted(dup_descs.items(), key=lambda kv: -len(kv[1])):
        print(f"  {d!r} ({len(fl)} pages):")
        for f in fl:
            print(f"    {f}")


if __name__ == "__main__":
    main()
