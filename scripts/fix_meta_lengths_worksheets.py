#!/usr/bin/env python3
"""Fixes title/description length across worksheets/*.html. Titles mostly follow
'{Name} Worksheet: Free Printable [with Teaching Guide] | Teachings.ai' (too
long); descriptions mostly follow 'Free printable ... with a clear learning
objective, difficulty level, and instructions for teachers and parents.' (too
long). A handful are bespoke. New copy is hand-written per file below and
verified to land in [50,60] / [140,155] before writing.
"""
import re
import sys

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 140, 155

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+[^>]*name=["\']description["\'][^>]*content=)(["\'])(.*?)\2', re.S | re.I)

# file -> (new_title or None, new_description or None)
CHANGES = {
    "worksheets/abc-flashcards.html": (
        "ABC Flashcards Worksheet: Free Printable | Teachings.ai",
        "Free printable ABC flashcards with a clear learning objective and full instructions for teachers and parents on how to use them well in class.",
    ),
    "worksheets/abc-mixed-review-activity.html": (
        "ABC Mixed Review Worksheet: Free Printable | Teachings.ai",
        "Free printable ABC mixed review worksheet combining several alphabet skills in one sheet, with instructions for teachers and parents to use.",
    ),
    "worksheets/addition-subtraction-practice.html": (
        "Addition & Subtraction Worksheet: Printable | Teachings.ai",
        "Free printable addition and subtraction practice worksheet with a learning objective, difficulty level, and self-checking strategies included.",
    ),
    "worksheets/alphabet-bubble-letter-workbook.html": (
        "Bubble Letter Coloring & Trace Workbook | Teachings.ai",
        "Free printable A-Z bubble letter coloring pages with separate tracing boxes for uppercase and lowercase letters, plus teacher and parent tips.",
    ),
    "worksheets/alphabet-tracing-and-coloring.html": (
        "Alphabet Tracing & Coloring: Printable | Teachings.ai",
        "Free printable alphabet tracing and coloring worksheet with a clear learning objective, difficulty level, and instructions for both teachers and parents.",
    ),
    "worksheets/alphabet-tracing.html": (
        "Alphabet Tracing Worksheet: Printable | Teachings.ai",
        "Free printable uppercase letter tracing worksheet with a clear learning objective, difficulty level, and instructions for both teachers and parents.",
    ),
    "worksheets/basic-cutting-skills.html": (
        "Cutting Skills Worksheet: Scissor Practice | Teachings.ai",
        "Free printable scissor cutting practice worksheet with a learning objective, difficulty level, safety tips, and teacher and parent instructions.",
    ),
    "worksheets/color-matching-with-real-photos.html": (
        "Color Matching with Real Photos: Printable | Teachings.ai",
        "Free printable color matching worksheet using real photographs instead of drawings, with a clear learning objective for teachers and parents.",
    ),
    "worksheets/color-word-matching-worksheet.html": (
        "Color Word Matching: Objects by Color | Teachings.ai",
        "Free printable worksheet grouping real-world objects by shared color and tracing each color word, building vocabulary and word recognition skills.",
    ),
    "worksheets/colouring-sheets.html": (
        "Colouring Sheets: Free Printable Guide | Teachings.ai",
        "Free printable colouring worksheet with a clear learning objective and instructions for teachers and parents, building color recognition skills.",
    ),
    "worksheets/count-and-match.html": (
        "Count and Match: Free Printable Guide | Teachings.ai",
        "Free printable count-and-match worksheet with a clear learning objective, difficulty level, an answer key, and instructions for teachers and parents.",
    ),
    "worksheets/counting-and-number-recognition.html": (
        "Counting & Number Recognition: Free Printable | Teachings.ai",
        "Free printable counting and number recognition worksheet with a clear learning objective, difficulty level, and instructions for teachers and parents.",
    ),
    "worksheets/counting-practice-how-many.html": (
        "Counting Practice: How Many? Free Printable | Teachings.ai",
        "Free printable multiple-choice counting worksheet: count objects and finger-counting hand pictures up to 20, then circle the correct number shown.",
    ),
    "worksheets/fruit-themed-coloring-book.html": (
        "Fruit-Themed Coloring Book: Printable Pages | Teachings.ai",
        "Free printable 30-page fruit-themed coloring book with detailed illustrated scenes, built for open-ended creative coloring and fine motor fun.",
    ),
    "worksheets/fruits-coloring-and-learning.html": (
        "Fruits Coloring & Learning: Printable | Teachings.ai",
        "Free printable fruits coloring and vocabulary worksheet with a clear learning objective, difficulty level, and instructions for teachers and parents.",
    ),
    "worksheets/fruits-vocabulary-matching.html": (
        "Fruits Vocabulary Matching: Printable | Teachings.ai",
        "Free printable worksheet matching fruit names to pictures, with a clear learning objective and instructions for both teachers and parents to use it well.",
    ),
    "worksheets/index.html": (
        "Worksheets Library: Free Printables & Teaching Tips",
        "Free printable worksheets, each with a real learning objective, difficulty level, and teacher and parent instructions — not just a raw PDF download.",
    ),
    "worksheets/learn-drawing.html": (
        "Learn Drawing Worksheet: Free Printable Guide | Teachings.ai",
        "Free printable learn-to-draw worksheet covering pre-writing strokes and creative expression, with a learning objective for teachers and parents.",
    ),
    "worksheets/letter-animal-coloring-pages.html": (
        'Letter & Animal Coloring Pages: "A is for..." | Teachings.ai',
        "Free printable A-Z coloring pages pairing each letter with a cute animal and an 'Aa is for ant' phrase to trace, building letter-sound vocabulary.",
    ),
    "worksheets/letter-sounds-coloring-trace-workbook.html": (
        None,
        "Free printable 26-page A-Z workbook pairing each letter with four objects starting with its sound, plus arrow guides and color-then-trace practice.",
    ),
    "worksheets/letter-sounds-worksheet.html": (
        "Letter Sounds Worksheet: Free Printable Guide | Teachings.ai",
        "Free printable letter sounds worksheet with a clear learning objective, difficulty level, and full instructions for both teachers and parents to use.",
    ),
    "worksheets/letter-writing-from-memory.html": (
        "Letter Writing from Memory: Free Printable | Teachings.ai",
        "Free printable letter writing from memory worksheet with a clear learning objective, difficulty level, and instructions for both teachers and parents.",
    ),
    "worksheets/lowercase-letter-tracing.html": (
        "Lowercase Letter Tracing Worksheet: Printable | Teachings.ai",
        "Free printable lowercase letter tracing worksheet with a clear learning objective, difficulty level, and instructions for both teachers and parents.",
    ),
    "worksheets/math-mixed-review-activity.html": (
        "Math Mixed Review Worksheet: Free Printable | Teachings.ai",
        "Free printable math mixed review worksheet combining counting, addition, and number recognition in one sheet, for teachers and parents to use.",
    ),
    "worksheets/number-mixed-review-activity.html": (
        "Number Mixed Review Worksheet: Free Printable | Teachings.ai",
        "Free printable number mixed review worksheet combining tracing, counting, and coloring in one sheet, with instructions for teachers and parents.",
    ),
    "worksheets/number-writing-practice.html": (
        "Number Writing Practice Worksheet: Printable | Teachings.ai",
        "Free printable number writing practice worksheet with a clear learning objective, difficulty level, and instructions for both teachers and parents.",
    ),
    "worksheets/numbers-1-to-10-activity-book.html": (
        "Numbers 1-10 Activity Book: Count & Trace | Teachings.ai",
        "Free printable Numbers 1-10 activity book combining directional tracing, object counting, a maze, a number search, and number-word tracing pages.",
    ),
    "worksheets/numbers-1-to-12-tracing-pack.html": (
        "Numbers 1-12 Tracing Pack: ASL & Matching | Teachings.ai",
        "Free printable Numbers 1-12 tracing pack combining repetition trace grids, a maze, ASL hand-sign pictures, and a number-word matching page too.",
    ),
    "worksheets/preschool-readiness-activity-pack.html": (
        "Preschool Readiness Activity Pack: Printable | Teachings.ai",
        "Free printable preschool readiness pack spanning letters, numbers, shapes, and colors all in one packet, with helpful tips for teachers and parents.",
    ),
    "worksheets/sentence-building-with-letters.html": (
        "Sentence Building with Letters: Printable | Teachings.ai",
        "Free printable sentence building worksheet that uses traced letters to form simple words and sentences, with tips for teachers and parents to guide.",
    ),
    "worksheets/shapes-activity.html": (
        "Shapes Activity: Free Printable Guide | Teachings.ai",
        "Free printable shapes activity worksheet with a clear learning objective, difficulty level, an answer key, and instructions for teachers and parents.",
    ),
    "worksheets/shapes-tracing-and-coloring.html": (
        "Shapes Tracing & Coloring: Printable | Teachings.ai",
        "Free printable shapes tracing and coloring worksheet with a clear learning objective, difficulty level, and instructions for both teachers and parents.",
    ),
    "worksheets/symmetry-practice.html": (
        "Symmetry Worksheet: Free Printable Practice | Teachings.ai",
        "Free printable symmetry worksheet building visual-spatial reasoning and pattern completion, with a learning objective for teachers and parents.",
    ),
    "worksheets/symmetry-tracing-and-coloring.html": (
        "Symmetry Tracing & Coloring: Free Printable | Teachings.ai",
        "Free printable symmetry tracing and coloring worksheet with a clear learning objective, difficulty level, and instructions for both teachers and parents.",
    ),
    "worksheets/three-digit-number-practice.html": (
        "Three-Digit Number Practice: Free Printable | Teachings.ai",
        "Free printable three-digit number worksheet covering place value and multi-digit reading and writing, for teachers and parents to guide practice.",
    ),
    "worksheets/uppercase-lowercase-matching.html": (
        "Uppercase & Lowercase Matching: Printable | Teachings.ai",
        "Free printable worksheet for matching uppercase letters to their lowercase pairs, with a clear learning objective for teachers and parents to use.",
    ),
    "worksheets/word-detective.html": (
        "Word Detective Worksheet: Free CVC Printable | Teachings.ai",
        "Free printable Word Detective worksheet for practicing simple CVC word reading, with a learning objective and instructions for teachers and parents.",
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
        print(f"[OK] {fname}")
        if new_title is not None:
            print(f"    title({len(new_title)}): {new_title}")
        if new_desc is not None:
            print(f"    desc ({len(new_desc)}): {new_desc}")

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

    print(f"\nok={ok} bad_len={bad} (dry_run={dry_run})")


if __name__ == "__main__":
    main()
