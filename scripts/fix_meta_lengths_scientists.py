#!/usr/bin/env python3
"""Fixes title/description length across learn/scientists/*.html (excluding index.html)."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

NEW_TITLES = {
    "alexander-graham-bell": "Alexander Graham Bell for Kids: Life & Fun Facts Too",
    "robert-oppenheimer": "J. Robert Oppenheimer for Kids: Life & Fun Facts Too",
}

NEW_DESCS = {
    "alexander-graham-bell": "Learn about Alexander Graham Bell, famous for inventing the telephone. Fun facts about this great scientist and STEM hero for curious young kids.",
    "antoine-lavoisier": "Learn about Antoine Lavoisier, famous for discovering that burning and breathing use oxygen. Fun facts about this great scientist and STEM hero for kids.",
    "charles-darwin": "Learn about Charles Darwin, famous for explaining how animals and plants change over time. Fun facts about this great scientist and STEM hero for kids.",
    "gustave-eiffel": "Learn about Gustave Eiffel, famous for designing the Eiffel Tower in Paris, France. Fun facts about this great scientist and STEM hero for kids.",
    "isaac-newton": "Learn about Isaac Newton, famous for discovering the laws of gravity and motion. Fun facts about this great scientist and STEM hero for kids.",
    "leonardo-da-vinci": "Learn about Leonardo da Vinci, famous for painting famous art and sketching future inventions. Fun facts about this great scientist and STEM hero for kids.",
    "nikola-tesla": "Learn about Nikola Tesla, famous for developing AC electricity that powers our homes. Fun facts about this great scientist and STEM hero for kids.",
    "robert-oppenheimer": "Learn about J. Robert Oppenheimer, famous for leading scientists studying nuclear physics. Fun facts about this great STEM hero for curious kids.",
    "srinivasa-ramanujan": "Learn about Srinivasa Ramanujan, famous for discovering thousands of amazing math formulas. Fun facts about this great scientist and STEM hero for kids.",
    "thomas-edison": "Learn about Thomas Edison, famous for inventing the light bulb and the phonograph. Fun facts about this great scientist and STEM hero for kids.",
}

ALL_SLUGS = [
    "alexander-graham-bell", "antoine-lavoisier", "charles-darwin", "gustave-eiffel",
    "isaac-newton", "leonardo-da-vinci", "nikola-tesla", "robert-oppenheimer",
    "srinivasa-ramanujan", "thomas-edison",
]


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for slug in ALL_SLUGS:
        fname = f"learn/scientists/{slug}.html"
        new_title = NEW_TITLES.get(slug)
        new_desc = NEW_DESCS.get(slug)
        if new_title is not None and not (TITLE_MIN <= len(new_title) <= TITLE_MAX):
            print(f"[BAD TITLE LEN {len(new_title)}] {fname}: {new_title}")
            bad += 1
            continue
        if new_desc is not None and not (DESC_MIN <= len(new_desc) <= DESC_MAX):
            print(f"[BAD DESC LEN {len(new_desc)}] {fname}: {new_desc}")
            bad += 1
            continue
        ok += 1
        print(f"[{'DRY' if dry_run else 'OK'}] {fname} title={len(new_title) if new_title else 'unchanged'} desc={len(new_desc) if new_desc else 'unchanged'}")
        if dry_run:
            continue
        src = open(fname, encoding="utf-8").read()
        if new_title is not None:
            tm = TITLE_RE.search(src)
            src = src[: tm.start(1)] + new_title.replace("&", "&amp;") + src[tm.end(1):]
        if new_desc is not None:
            dm = DESC_RE.search(src)
            src = src[: dm.start(3)] + new_desc.replace("&", "&amp;") + src[dm.end(3):]
        with open(fname, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
    print(f"\nok={ok} bad={bad} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
