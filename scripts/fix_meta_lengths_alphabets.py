#!/usr/bin/env python3
"""Fixes title/description length for the learn/alphabets/letter-*.html and
index.html pages. Two sub-groups share different templates:
- letter-a..letter-i: title AND description both too long -> shorten both.
- letter-j..letter-z: title already fine, description too short -> lengthen only.
- index.html: both too long -> shorten both.
"""
import re
import sys
import string

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)


def pick(candidates, lo, hi):
    in_range = [c for c in candidates if lo <= len(c) <= hi]
    if in_range:
        mid = (lo + hi) / 2
        return min(in_range, key=lambda c: abs(len(c) - mid))
    return min(candidates, key=lambda c: abs(len(c) - (lo + hi) / 2))


def title_for_a_to_i(letter):
    candidates = [
        f"Letter {letter} for Kids: Words, Pictures & Tracing",
        f"Letter {letter} for Kids – Words, Pictures & Tracing",
        f"Letter {letter} for Kids: Words, Pictures, Tracing & More",
    ]
    return pick(candidates, TITLE_MIN, TITLE_MAX)


def desc_for_a_to_i(letter):
    candidates = [
        f"Fun Letter {letter} activities for preschoolers: words starting with {letter}, tracing practice, pronunciation, and fun facts for early kindergarten learners.",
        f"Fun Letter {letter} activities for preschoolers: words starting with {letter}, tracing practice, pronunciation, fun facts, and colorful pictures for kindergarten.",
        f"Fun Letter {letter} activities for preschoolers: words starting with {letter}, tracing practice, pronunciation, and fun facts for kindergarten learners.",
    ]
    return pick(candidates, DESC_MIN, DESC_MAX)


def desc_for_j_to_z(letter):
    candidates = [
        f"Learn Letter {letter} for kids with words, pictures, pronunciation, tracing practice, and fun facts — a complete alphabet activity for early readers.",
        f"Learn Letter {letter} for kids with words, pictures, pronunciation, tracing practice, and fun facts — a complete kindergarten alphabet activity.",
        f"Learn Letter {letter} for kids with words, pictures, pronunciation, and tracing practice — a complete kindergarten and preschool alphabet activity for early readers.",
    ]
    return pick(candidates, DESC_MIN, DESC_MAX)


def apply_change(fname, new_title, new_desc, dry_run):
    src = open(fname, encoding="utf-8").read()
    tm = TITLE_RE.search(src)
    dm = DESC_RE.search(src)
    old_title = tm.group(1).strip() if tm else None
    old_desc = dm.group(3).strip() if dm else None

    ok_title = new_title is None or (TITLE_MIN <= len(new_title) <= TITLE_MAX)
    ok_desc = new_desc is None or (DESC_MIN <= len(new_desc) <= DESC_MAX)
    status = "ok" if (ok_title and ok_desc) else "out-of-range"

    print(f"[{'DRY' if dry_run else 'OK' if status=='ok' else 'OUT-OF-RANGE'}] {fname}")
    if new_title is not None:
        print(f"    title({len(new_title)}): {new_title}   [was: {old_title}]")
    if new_desc is not None:
        print(f"    desc ({len(new_desc)}): {new_desc}")

    if dry_run or status != "ok":
        return status

    if new_title is not None and tm:
        src = src[: tm.start(1)] + new_title.replace("&", "&amp;") + src[tm.end(1):]
        tm2 = TITLE_RE.search(src)  # not needed again but keep vars consistent
    if new_desc is not None:
        dm2 = DESC_RE.search(src)
        src = src[: dm2.start(3)] + new_desc.replace("&", "&amp;") + src[dm2.end(3):]

    with open(fname, "w", encoding="utf-8", newline="\n") as f:
        f.write(src)
    return status


def main():
    dry_run = "--dry-run" in sys.argv
    results = {"ok": 0, "out-of-range": 0}

    for letter in string.ascii_uppercase[:9]:  # A-I
        fname = f"learn/alphabets/letter-{letter.lower()}.html"
        t = title_for_a_to_i(letter)
        d = desc_for_a_to_i(letter)
        status = apply_change(fname, t, d, dry_run)
        results[status] += 1

    for letter in string.ascii_uppercase[9:]:  # J-Z
        fname = f"learn/alphabets/letter-{letter.lower()}.html"
        d = desc_for_j_to_z(letter)
        status = apply_change(fname, None, d, dry_run)
        results[status] += 1

    # index.html
    idx_title = pick([
        "Alphabet Learning for Kids: A to Z Fun, Facts & Games",
        "Complete Alphabet Learning for Kids: A to Z Fun & Games",
        "Alphabet Learning for Kids: A to Z Fun & Games",
    ], TITLE_MIN, TITLE_MAX)
    idx_desc = pick([
        "Master the ABCs! Explore all 26 letters with colorful pictures, fun words, and tracing activities. Great for preschool and kindergarten early readers.",
        "Explore all 26 letters from A to Z with pictures, fun words, and tracing activities — great for preschool and kindergarten early readers to master the ABCs.",
    ], DESC_MIN, DESC_MAX)
    status = apply_change("learn/alphabets/index.html", idx_title, idx_desc, dry_run)
    results[status] += 1

    print(f"\nok={results['ok']} out-of-range={results['out-of-range']} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
