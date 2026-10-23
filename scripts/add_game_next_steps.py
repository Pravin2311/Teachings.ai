"""
Adds a "Keep Learning" block of related lessons, games and printables to
the root game pages that already bring in search visitors.

Why: these games are the site's best search landing pages (Bing positions
~5-6, 67-81% engagement, highest AdSense revenue per page) but they were
dead ends -- apart from the footer there was no link out, so a child or
parent who finished the game had nowhere to go next. The block gives them
a next step and gives crawlers a path from these pages into the lessons.

Only the pages in NEXT_STEPS are changed; the other root game pages are
left as they are so they can serve as a comparison group (see
seo/experiments.json, game-next-steps). The block is inserted just before
the "<!-- Footer -->" comment (or before </body> on pages that have
no footer); the game itself is untouched. Re-running is
safe: pages that already have the block are skipped.

Usage:
  python scripts/add_game_next_steps.py [--dry-run]
"""
import html
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY_RUN = "--dry-run" in sys.argv
MARKER = "<!-- Keep Learning -->"
ANCHOR = "<!-- Footer -->"

# page -> [(href, link text)]; every href must exist in the repo
NEXT_STEPS = {
    "colors.html": [
        ("/learn/colors/index.html", "Colors for Kids: all 10 colors"),
        ("/learn/colors/red.html", "Red things for kids"),
        ("/learn/colors/blue.html", "Blue things for kids"),
        ("/learn/colors/yellow.html", "Yellow things for kids"),
        ("/colours-sorting.html", "Color Sorting game"),
        ("/worksheets/color-matching-with-real-photos.html", "Printable color matching worksheet"),
    ],
    "bodyparts.html": [
        ("/learn/body-parts/index.html", "Body Parts for Kids: lessons"),
        ("/learn/body-parts/eyes.html", "Eyes for kids"),
        ("/learn/body-parts/hands.html", "Hands for kids"),
        ("/organs.html", "Human Organs game"),
        ("/learn/organs/index.html", "Human body organs for kids"),
    ],
    "organs.html": [
        ("/learn/organs/index.html", "Human Body Organs for Kids: lessons"),
        ("/learn/organs/heart.html", "Heart for kids"),
        ("/learn/organs/brain.html", "Brain for kids"),
        ("/learn/organs/lungs.html", "Lungs for kids"),
        ("/bodyparts.html", "Body Parts game"),
    ],
    "patterns.html": [
        ("/learn/shapes/index.html", "Shapes for Kids: sides and corners"),
        ("/shapes.html", "Shapes matching game"),
        ("/match-shapes.html", "Shapes drag-and-drop game"),
        ("/colours-sorting.html", "Color Sorting game"),
        ("/counting.html", "Counting game"),
    ],
    "animals.html": [
        ("/learn/animals/index.html", "Animals for Kids: A to Z lessons"),
        ("/learn/birds/index.html", "Birds for kids"),
        ("/animals-birds-sorting.html", "Animals & Birds Sorting game"),
        ("/match-animals.html", "Animal Match game"),
    ],
    "counting.html": [
        ("/learn/numbers/index.html", "Numbers 0 to 10: lessons"),
        ("/match-numbers.html", "Number Match game"),
        ("/odd-even.html", "Odd & Even game"),
        ("/numbers.html", "Numbers scratch game"),
        ("/worksheets/counting-practice-how-many.html", "Printable counting worksheet"),
    ],
    "fruits-vegetables-sorting.html": [
        ("/learn/fruits/index.html", "Fruits for Kids: lessons"),
        ("/learn/vegetables/index.html", "Vegetables for Kids: lessons"),
        ("/fruits.html", "Fruits scratch game"),
        ("/vegetables.html", "Vegetables scratch game"),
    ],
    "match-numbers.html": [
        ("/learn/numbers/index.html", "Numbers 0 to 10: lessons"),
        ("/counting.html", "Counting game"),
        ("/odd-even.html", "Odd & Even game"),
        ("/worksheets/number-writing-practice.html", "Printable number writing worksheet"),
    ],
    "rhyming.html": [
        ("/phonic-rhyming.html", "Rhyming & Listening game"),
        ("/learn/phonics/index.html", "Phonics: A to Z letter sounds"),
        ("/word-matching.html", "Word Matching game"),
    ],
    # second batch (2026-10-23): full-screen games with no header or footer,
    # so the block goes just before </body>
    "mirror-words-learning.html": [
        ("/phonic-words.html", "Sound & Blend phonics game"),
        ("/sight.html", "Sight Words game"),
        ("/word-matching.html", "Word Matching game"),
        ("/learn/phonics/index.html", "Phonics: A to Z letter sounds"),
    ],
    "phonic-numbers.html": [
        ("/learn/numbers/index.html", "Numbers 0 to 10: lessons"),
        ("/numbers.html", "Numbers scratch game"),
        ("/match-numbers.html", "Number Match game"),
        ("/counting.html", "Counting game"),
    ],
    "phonic-rhyming.html": [
        ("/rhyming.html", "Rhyming words game"),
        ("/phonic-letter-sound.html", "Letter Sounds A to Z game"),
        ("/learn/phonics/index.html", "Phonics: A to Z letter sounds"),
        ("/word-matching.html", "Word Matching game"),
    ],
    "phonic-segmenting.html": [
        ("/phonic-words.html", "Sound & Blend phonics game"),
        ("/phonic-letter-sound.html", "Letter Sounds A to Z game"),
        ("/sight.html", "Sight Words game"),
        ("/learn/phonics/index.html", "Phonics: A to Z letter sounds"),
    ],
    "tracing-letters-and-numbers.html": [
        ("/learn/alphabets/index.html", "Alphabet A to Z: lessons"),
        ("/learn/numbers/index.html", "Numbers 0 to 10: lessons"),
        ("/worksheets/alphabet-tracing.html", "Printable alphabet tracing worksheet"),
        ("/worksheets/number-writing-practice.html", "Printable number writing worksheet"),
    ],
}
# pages without a "<!-- Footer -->" comment: insert before </body> instead
BODY_END = {"mirror-words-learning.html", "phonic-numbers.html", "phonic-rhyming.html",
            "phonic-segmenting.html", "tracing-letters-and-numbers.html"}

LINK_STYLE = ("display:inline-block;padding:12px 16px;background:#fff;border:1px solid #e0e0f0;"
              "border-radius:8px;color:#1B2A5B;text-decoration:none;font-weight:bold;"
              "box-shadow:0 2px 6px rgba(0,0,0,0.05);")


def block(links):
    items = "\n".join(f'    <li><a href="{href}" style="{LINK_STYLE}">{html.escape(text)}</a></li>'
                      for href, text in links)
    return (f"{MARKER}\n"
            f'<section class="next-steps-box" style="width:100%;box-sizing:border-box;max-width:640px;margin:20px auto;padding:0 24px;">\n'
            f'  <h2 style="font-size:1.25em;color:#1B2A5B;">📚 Keep Learning</h2>\n'
            f'  <ul style="list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:10px;">\n'
            f"{items}\n"
            f"  </ul>\n"
            f"</section>\n\n")


def main():
    missing = [(p, h) for p, links in NEXT_STEPS.items() for h, _ in links
               if not os.path.isfile(os.path.join(ROOT, h.lstrip("/")))]
    if missing:
        sys.exit(f"Link targets not found: {missing}")
    changed = []
    for page, links in NEXT_STEPS.items():
        fp = os.path.join(ROOT, page)
        with open(fp, encoding="utf-8", newline="") as fh:
            src = fh.read()
        if MARKER in src:
            continue
        anchor = "</body>" if page in BODY_END else ANCHOR
        if src.count(anchor) != 1:
            print(f"SKIP {page}: expected exactly one {anchor}")
            continue
        new = src.replace(anchor, block(links) + anchor, 1)
        changed.append(page)
        if not DRY_RUN:
            with open(fp, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Pages updated: {len(changed)}")
    for p in changed:
        print(f"  {p}")


if __name__ == "__main__":
    main()
