#!/usr/bin/env python3
"""Fixes title/description length across science/*.html. Bespoke articles,
hand-trimmed per file."""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

CHANGES = {
    "science/index.html": (
        "Science Activities: Hands-On Experiments & Observation",
        "Hands-on science activities for kids — kitchen experiments, the scientific method, nature journaling, and weather watching, with real explanations.",
    ),
    "science/life-cycles-from-egg-to-adult.html": (
        "Life Cycles: From Egg to Adult for Young Scientists",
        None,
    ),
    "science/magnets-and-static-electricity.html": (
        None,
        "Safe, simple magnet and static electricity experiments for kids — testing what's magnetic, a balloon-and-hair demo, and the science behind each one.",
    ),
    "science/nature-journaling-for-beginners.html": (
        "Nature Journaling for Beginners: A Simple Starter Guide",
        None,
    ),
    "science/simple-kitchen-science-experiments.html": (
        None,
        "Safe, simple science experiments using kitchen ingredients — baking soda reactions, density towers, and more — with real explanations of the science.",
    ),
    "science/simple-machines-for-kids.html": (
        "Simple Machines for Kids: The Six Basic Machines Too",
        "An introduction to the six simple machines — lever, wheel and axle, pulley, inclined plane, wedge, and screw — with household examples to try.",
    ),
    "science/teaching-the-scientific-method.html": (
        None,
        "A kid-friendly breakdown of the scientific method — question, hypothesis, test, observe, conclude — with age-appropriate ways to practice at home.",
    ),
    "science/weather-watching-activities.html": (
        None,
        "Simple weather tracking and observation activities for kids — homemade weather tools, a daily tracking chart, and how to connect weather to climate.",
    ),
}


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad = 0, 0
    for fname, (new_title, new_desc) in CHANGES.items():
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
