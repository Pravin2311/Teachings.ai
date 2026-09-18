#!/usr/bin/env python3
"""Batch-shortens/lengthens title + meta description for the learn/vehicles and
learn/electronics 'item detail' page clusters, which share a near-identical
template. Extracts the per-item name + fact clause already present in the page,
splices them into a new template sized to land in the target windows, and only
writes a file if BOTH the new title (50-60 chars) and description (140-155
chars) land in range -- otherwise it's left untouched and reported for manual
follow-up.

Run with --dry-run first to see projected lengths before writing anything.
"""
import re
import sys
import html

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

FILES = [
    # learn/vehicles item-detail pages (transportation template)
    "learn/vehicles/articulated-bus.html", "learn/vehicles/bullet-train.html",
    "learn/vehicles/cargo-plane.html", "learn/vehicles/cargo-ship.html",
    "learn/vehicles/concrete-mixer.html", "learn/vehicles/cruise-bike.html",
    "learn/vehicles/cruise-ship.html", "learn/vehicles/diesel-train.html",
    "learn/vehicles/dirt-bike.html", "learn/vehicles/double-decker.html",
    "learn/vehicles/dump-truck.html", "learn/vehicles/electric-bus.html",
    "learn/vehicles/electric-moto.html", "learn/vehicles/electric-train.html",
    "learn/vehicles/fighter-jet.html", "learn/vehicles/fire-truck.html",
    "learn/vehicles/garbage-truck.html", "learn/vehicles/glider.html",
    "learn/vehicles/medical-heli.html", "learn/vehicles/military-heli.html",
    "learn/vehicles/motorboat.html", "learn/vehicles/police-heli.html",
    "learn/vehicles/private-jet.html", "learn/vehicles/scooter.html",
    "learn/vehicles/seaplane.html", "learn/vehicles/steam-train.html",
    "learn/vehicles/tow-truck.html",
    # learn/electronics item-detail pages (STEM template)
    "learn/electronics/calculator.html", "learn/electronics/camera.html",
    "learn/electronics/cctv.html", "learn/electronics/charger.html",
    "learn/electronics/computer-mouse.html", "learn/electronics/earpod.html",
    "learn/electronics/flashlight.html", "learn/electronics/game-controller.html",
    "learn/electronics/headphone.html", "learn/electronics/keyboard.html",
    "learn/electronics/memory-card.html", "learn/electronics/monitor.html",
    "learn/electronics/satellite-antenna.html", "learn/electronics/self-driving-car.html",
    "learn/electronics/sim-card.html", "learn/electronics/smart-watch.html",
    "learn/electronics/solar-pannel.html", "learn/electronics/speaker.html",
    "learn/electronics/usb-pendrive.html", "learn/electronics/video-camera.html",
    "learn/electronics/voice-assistant.html",
]

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)
# "Learn about the X! Discover how it works and fun facts about Y. Perfect for ... STEM learning."
DESC_PAT_A = re.compile(
    r"^Learn about the (?P<name>.+?)! Discover how it works and fun facts about (?P<clause>.+?)\.\s*Perfect for preschool and kindergarten STEM learning\.$"
)
# "Learn all about the X! Discover fun facts about Y. Perfect for ... transportation learning."
DESC_PAT_B = re.compile(
    r"^Learn all about the (?P<name>.+?)! Discover fun facts about (?P<clause>.+?)\.\s*Perfect for preschool and kindergarten transportation learning\.$"
)


def build_title(name):
    prefixes = ["", "The "]
    joins = [": ", " — ", " - "]
    suffixes = [
        "How It Works & Fun Facts",
        "How It Works, Uses & Fun Facts",
        "How It Works, Uses & Facts",
        "Uses, How It Works & Fun Facts",
        "How It Works & Cool Fun Facts",
    ]
    candidates = [
        f"{p}{name} for Kids{j}{s}"
        for p in prefixes for j in joins for s in suffixes
    ]
    in_range = [c for c in candidates if TITLE_MIN <= len(c) <= TITLE_MAX]
    if in_range:
        mid = (TITLE_MIN + TITLE_MAX) / 2
        return min(in_range, key=lambda c: abs(len(c) - mid))
    return min(candidates, key=lambda c: abs(len(c) - (TITLE_MIN + TITLE_MAX) / 2))


def build_desc(name, clause, stem):
    openings = [f"Learn about the {name}!", f"Meet the {name}!", f"Discover the {name}!"]
    bodies = [
        f"Discover fun facts about {clause}.",
        f"It's used for {clause}.",
        f"Learn how it helps with {clause}.",
        f"See how it works: {clause}.",
    ]
    tails = [
        "Great for preschool and kindergarten STEM learning." if stem else "Great for preschool and kindergarten learners.",
        "Fun for preschool and kindergarten learners." if not stem else "Fun for preschool and kindergarten STEM learning.",
        "Perfect for preschool and kindergarten learners." if not stem else "Perfect for preschool and kindergarten STEM learning.",
        "A fun pick for preschool and kindergarten learners." if not stem else "A fun pick for preschool and kindergarten STEM fans.",
    ]
    candidates = [f"{o} {b} {t}" for o in openings for b in bodies for t in tails]
    in_range = [c for c in candidates if DESC_MIN <= len(c) <= DESC_MAX]
    if in_range:
        mid = (DESC_MIN + DESC_MAX) / 2
        return min(in_range, key=lambda c: abs(len(c) - mid))
    return min(candidates, key=lambda c: abs(len(c) - (DESC_MIN + DESC_MAX) / 2))


def process(fname, dry_run):
    src = open(fname, encoding="utf-8").read()
    tm = TITLE_RE.search(src)
    dm = DESC_RE.search(src)
    if not tm or not dm:
        return ("no-match", fname, None, None)

    old_title = html.unescape(tm.group(1).strip())
    old_desc = html.unescape(dm.group(3).strip())

    name_from_title = re.match(r"^(.+?) for Kids", old_title)
    name = name_from_title.group(1).strip() if name_from_title else None

    m = DESC_PAT_A.match(old_desc)
    stem = True
    if not m:
        m = DESC_PAT_B.match(old_desc)
        stem = False
    if not m or not name:
        return ("no-match", fname, old_title, old_desc)

    clause = m.group("clause")
    new_title = build_title(name)
    new_desc = build_desc(name, clause, stem)

    ok_title = TITLE_MIN <= len(new_title) <= TITLE_MAX
    ok_desc = DESC_MIN <= len(new_desc) <= DESC_MAX

    status = "ok" if (ok_title and ok_desc) else "out-of-range"

    if status == "ok" and not dry_run:
        new_src = src[: tm.start(1)] + html.escape(new_title, quote=False) + src[tm.end(1):]
        # re-find desc offsets in new_src since title length may differ
        dm2 = DESC_RE.search(new_src)
        new_src = new_src[: dm2.start(3)] + html.escape(new_desc, quote=False) + new_src[dm2.end(3):]
        with open(fname, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_src)

    return (status, fname, new_title, new_desc)


def main():
    dry_run = "--dry-run" in sys.argv
    ok, bad, nomatch = 0, 0, 0
    for fname in FILES:
        status, f, new_title, new_desc = process(fname, dry_run)
        if status == "ok":
            ok += 1
            marker = "[DRY]" if dry_run else "[OK] "
            print(f"{marker} {f}")
            print(f"       title({len(new_title)}): {new_title}")
            print(f"       desc ({len(new_desc)}): {new_desc}")
        elif status == "out-of-range":
            bad += 1
            print(f"[OUT-OF-RANGE] {f}")
            print(f"       title({len(new_title)}): {new_title}")
            print(f"       desc ({len(new_desc)}): {new_desc}")
        else:
            nomatch += 1
            print(f"[NO-MATCH] {f}")
    print(f"\nok={ok} out-of-range={bad} no-match={nomatch} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
