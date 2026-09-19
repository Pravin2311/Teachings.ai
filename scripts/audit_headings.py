"""
H1 is one of the strongest on-page relevance signals left unchecked this
session. Audits every page for: missing H1, multiple H1s (dilutes
relevance / confuses which is the "real" heading), and an H1 that's
suspiciously generic or doesn't share any real word with the <title>
(a sign the page's heading and its search snippet are telling Google
two different things about what the page is).
"""
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}

H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
STOPWORDS = {"the", "a", "an", "for", "and", "to", "of", "kids", "|", "-", "teachings.ai", "with"}


def clean(text):
    text = TAG_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def words(text):
    return {w.lower().strip(".,!?:;'\"") for w in text.split() if w.lower() not in STOPWORDS and len(w) > 2}


def main():
    no_h1, multi_h1, mismatch = [], [], []
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
                continue  # redirect stub
            total += 1
            rel = os.path.relpath(fp, ROOT).replace("\\", "/")

            h1s = [clean(m) for m in H1_RE.findall(content)]
            h1s = [h for h in h1s if h]
            if not h1s:
                no_h1.append(rel)
                continue
            if len(h1s) > 1:
                multi_h1.append((rel, len(h1s)))

            tmatch = TITLE_RE.search(content)
            if tmatch:
                title = clean(tmatch.group(1))
                h1_words = words(h1s[0])
                title_words = words(title)
                if h1_words and title_words and not (h1_words & title_words):
                    mismatch.append((rel, h1s[0][:60], title[:60]))

    print(f"Total pages checked: {total}")
    print(f"Missing H1: {len(no_h1)}")
    print(f"Multiple H1s: {len(multi_h1)}")
    print(f"H1/<title> share no common word: {len(mismatch)}")
    print()
    print("=== MISSING H1 ===")
    for p in no_h1:
        print(f"  {p}")
    print("\n=== MULTIPLE H1 ===")
    for p, n in multi_h1:
        print(f"  {p}: {n} H1 tags")
    print("\n=== H1/TITLE MISMATCH (first 30) ===")
    for p, h1, t in mismatch[:30]:
        print(f"  {p}\n    H1:    {h1}\n    Title: {t}")


if __name__ == "__main__":
    main()
