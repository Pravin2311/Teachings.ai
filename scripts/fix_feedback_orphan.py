"""
feedback.html has 0 inbound internal links (confirmed via audit_internal_links.py):
the shared footer's "Contact Us" button is a mailto: link that bypasses the
dedicated feedback.html landing page entirely, so nothing ever points to it.

Fix: add a "Feedback" link to /feedback.html in the same footer-nav block,
right after the Disclaimer link, matching each file's existing indentation.
Does not touch the existing mailto Contact Us button.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY_RUN = "--dry-run" in sys.argv

PATTERN = re.compile(
    r'([ \t]*)<a href="/disclaimer\.html" class="blog-button">Disclaimer</a>\r?\n'
)


def main():
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {"mockups", ".git", "node_modules"} and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            if "/feedback.html" in content:
                continue
            m = PATTERN.search(content)
            if not m:
                continue
            indent = m.group(1)
            insertion = f'{indent}<a href="/feedback.html" class="blog-button">Feedback</a>\n'
            new_content = content[: m.end()] + insertion + content[m.end():]
            rel = os.path.relpath(fp, ROOT).replace("\\", "/")
            changed.append(rel)
            if not DRY_RUN:
                with open(fp, "w", encoding="utf-8", newline="") as fh:
                    fh.write(new_content)

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Added Feedback footer link to {len(changed)} pages")
    for f in changed:
        print(f"  {f}")


if __name__ == "__main__":
    main()
