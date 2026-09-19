"""
AI Overview citation eligibility leans heavily on FAQPage schema for
pages that already answer common questions -- Google (and AI answer
engines generally) can lift a marked-up Q&A pair directly into a
citation. Finds pages with a visible "Frequently Asked Questions" (or
similar) section in their actual content that AREN'T backed by
FAQPage schema -- a real, free citation opportunity, not a new content
task, since the Q&A text already exists on the page.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}

FAQ_HEADING_RE = re.compile(
    r"<h[234][^>]*>[^<]*(?:frequently asked questions|faqs?\b)[^<]*</h[234]>",
    re.IGNORECASE,
)


def main():
    has_heading_no_schema = []
    has_both = 0
    total = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            if "http-equiv=\"refresh\"" in content[:500]:
                continue
            total += 1
            has_heading = bool(FAQ_HEADING_RE.search(content))
            has_schema = "FAQPage" in content
            if has_heading and not has_schema:
                rel = os.path.relpath(fp, ROOT).replace("\\", "/")
                has_heading_no_schema.append(rel)
            elif has_heading and has_schema:
                has_both += 1

    print(f"Total pages checked: {total}")
    print(f"Pages with a visible FAQ heading AND FAQPage schema: {has_both}")
    print(f"Pages with a visible FAQ heading but NO FAQPage schema: {len(has_heading_no_schema)}")
    print()
    for p in has_heading_no_schema:
        print(f"  {p}")


if __name__ == "__main__":
    main()
