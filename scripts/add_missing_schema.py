#!/usr/bin/env python3
"""Adds a JSON-LD schema block to pages that currently have none, using
values already established in each page's title/description/canonical
(all previously verified). Game pages get LearningResource, the phonics
hub gets CollectionPage, and simple utility pages get WebPage.
"""
import re
import sys

CANONICAL_RE = re.compile(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=(["\'])(.*?)\1', re.S | re.I)

GAMES = {
    "flags-of-the-countries.html": (
        "Flags of the Countries Game",
        "Interactive scratch-to-reveal game where kids learn world flags and geography.",
        ["Preschool", "Kindergarten"],
    ),
    "match-numbers.html": (
        "Number Match Game",
        "Fun drag-and-drop number-to-image matching game for kids aged 3-6.",
        ["Preschool", "Kindergarten"],
    ),
    "match-shapes.html": (
        "Shapes Match Game",
        "Fun drag-and-drop shape matching game using real pictures for kids aged 3-6.",
        ["Preschool", "Kindergarten"],
    ),
    "match-words.html": (
        "Word Match Game",
        "Fun drag-and-drop word-to-picture matching game for kids aged 3-6.",
        ["Preschool", "Kindergarten"],
    ),
    "mirror-words-learning.html": (
        "Reflection Words Game",
        "A playful game where kids learn how words look when reversed (NET to TEN).",
        ["Preschool", "Kindergarten"],
    ),
    "phonic-rhyming.html": (
        "Rhyming & Listening Game",
        "A rhyming and listening game for kids ages 3-7 to build phonemic awareness.",
        ["Preschool", "Kindergarten"],
    ),
    "shapes.html": (
        "Basic Shapes Matching Game",
        "Fun and interactive shape matching games for kids that build shape recognition.",
        ["Preschool", "Kindergarten"],
    ),
    "tracing-letters-and-numbers.html": (
        "Tracing Letters & Numbers",
        "An interactive tracing app for kids to learn ABC letters and numbers.",
        ["Preschool", "Kindergarten"],
    ),
}

HUBS = {
    "phonics.html": (
        "Phonics Games Hub",
        "A hub of free phonics games for kids: sound blending, letter-sound matching, phonic numbers, and word building.",
    ),
}

WEBPAGES = {
    "Blog/index.html": ("Teachings.AI Blog", "Tips, updates, and fun learning ideas for parents, teachers, and kids."),
    "about.html": ("About Teachings.AI", "Teachings.AI's mission, vision, and story."),
    "disclaimer.html": ("Disclaimer & Affiliate Disclosure", "Disclaimer and affiliate disclosure for Teachings.AI."),
    "feedback.html": ("Feedback & Contact Us", "Share feedback, report a bug, or suggest a new activity for Teachings.ai."),
    "privacy-policy.html": ("Privacy Policy", "Privacy Policy for Teachings.AI."),
    "reels.html": ("Learning Reels for Kids", "Bite-sized educational video reels for kids."),
}


def build_game_schema(url, name, desc, levels):
    levels_json = ", ".join(f'"{l}"' for l in levels)
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LearningResource",
  "name": "{name}",
  "description": "{desc}",
  "educationalLevel": [{levels_json}],
  "inLanguage": "en",
  "url": "{url}",
  "isAccessibleForFree": true,
  "publisher": {{
    "@type": "Organization",
    "name": "Teachings.AI",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://www.teachings.ai/assets/images/app_logo.png"
    }}
  }}
}}
</script>
'''


def build_hub_schema(url, name, desc):
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "{name}",
  "description": "{desc}",
  "url": "{url}",
  "publisher": {{
    "@type": "Organization",
    "name": "Teachings.AI",
    "url": "https://www.teachings.ai"
  }}
}}
</script>
'''


def build_webpage_schema(url, name, desc):
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "{name}",
  "description": "{desc}",
  "url": "{url}",
  "isPartOf": {{
    "@type": "WebSite",
    "name": "Teachings.AI",
    "url": "https://www.teachings.ai"
  }}
}}
</script>
'''


def insert(fname, schema_block, dry_run):
    src = open(fname, encoding="utf-8").read()
    if "application/ld+json" in src:
        print(f"[SKIP already-has-schema] {fname}")
        return False
    head_close = re.search(r"</head>", src, re.I)
    if not head_close:
        print(f"[NO </head> FOUND] {fname}")
        return False
    insert_pos = head_close.start()
    new_src = src[:insert_pos] + schema_block + src[insert_pos:]
    print(f"[{'DRY' if dry_run else 'OK'}] {fname}")
    if not dry_run:
        with open(fname, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_src)
    return True


def main():
    dry_run = "--dry-run" in sys.argv
    count = 0

    for fname, (name, desc, levels) in GAMES.items():
        src = open(fname, encoding="utf-8").read()
        cm = CANONICAL_RE.search(src)
        url = cm.group(2) if cm else f"https://www.teachings.ai/{fname}"
        if insert(fname, build_game_schema(url, name, desc, levels), dry_run):
            count += 1

    for fname, (name, desc) in HUBS.items():
        src = open(fname, encoding="utf-8").read()
        cm = CANONICAL_RE.search(src)
        url = cm.group(2) if cm else f"https://www.teachings.ai/{fname}"
        if insert(fname, build_hub_schema(url, name, desc), dry_run):
            count += 1

    for fname, (name, desc) in WEBPAGES.items():
        src = open(fname, encoding="utf-8").read()
        cm = CANONICAL_RE.search(src)
        url = cm.group(2) if cm else f"https://www.teachings.ai/{fname}"
        if insert(fname, build_webpage_schema(url, name, desc), dry_run):
            count += 1

    print(f"\nadded={count} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
