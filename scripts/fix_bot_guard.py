"""
Stops automated browsers from being counted in GA4 or loading AdSense.

Since 2026-10-16 most GA4 "Direct" users have been scripted visits (Ashburn
and Singapore data centres, ~60 s sessions, 0% engagement; see
seo/reports/2026-10-29-ga4-direct.md). Browsers driven by Selenium,
Puppeteer or Playwright set navigator.webdriver = true. This script swaps
each page's static loaders

    <script async src=".../gtag/js?id=G-XVYMNTZLQJ"></script>
    <script> dataLayer ... gtag('js') ... gtag('config', ...) </script>
    <script async src=".../adsbygoogle.js?client=..." crossorigin="anonymous"></script>

for one inline block that always defines dataLayer and gtag() (so the
gtag('event') calls in index.html and js/script.js never throw), and only
sends the config and injects gtag.js and adsbygoogle.js when
navigator.webdriver is not set. A page with no AdSense loader gets the guard
without the ads line. The ad <ins> slots and their push({}) calls stay as
they are: with no adsbygoogle.js they stay empty, at zero height.

It does not catch bots that hide the flag; it only removes the easy ones.

Usage:
  python scripts/fix_bot_guard.py [--dry-run] [--exclude REGEX]

--exclude skips pages whose repo-relative path matches REGEX (e.g. pages
inside a running SEO experiment that shouldn't change yet). Re-running is
safe: pages that already have the guard are skipped.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", "seo", ".git", "node_modules"}
DRY_RUN = "--dry-run" in sys.argv
EXCLUDE = re.compile(sys.argv[sys.argv.index("--exclude") + 1]) if "--exclude" in sys.argv else None

GA_ID = "G-XVYMNTZLQJ"
AD_CLIENT = "ca-pub-7495143337429327"
MARKER = "bot-guard:"

# gtag.js tag followed by its inline config block (three whitespace variants on the site).
GA_RE = re.compile(
    r'[ \t]*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=' + re.escape(GA_ID) + r'"></script>[ \t]*\r?\n'
    r'[ \t]*<script>\s*window\.dataLayer = window\.dataLayer \|\| \[\];\s*'
    r'function gtag\(\)\s*\{\s*dataLayer\.push\(arguments\);\s*\}\s*'
    r"gtag\('js', new Date\(\)\);\s*gtag\('config', '" + re.escape(GA_ID) + r"'\);\s*</script>[ \t]*\r?\n?"
)
AD_RE = re.compile(
    r'[ \t]*<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client='
    + re.escape(AD_CLIENT) + r'" crossorigin="anonymous"></script>[ \t]*\r?\n?'
)


def guard(with_ads, nl):
    lines = [
        "  <script>",
        "    // " + MARKER + " automated browsers (navigator.webdriver) get no GA4 or AdSense. See scripts/fix_bot_guard.py.",
        "    window.dataLayer = window.dataLayer || [];",
        "    function gtag(){dataLayer.push(arguments);}",
        "    (function () {",
        "      if (navigator.webdriver) return;",
        "      function load(src, cors) { var s = document.createElement('script'); s.async = true; s.src = src; if (cors) s.crossOrigin = 'anonymous'; document.head.appendChild(s); }",
        "      gtag('js', new Date());",
        "      gtag('config', '" + GA_ID + "');",
        "      load('https://www.googletagmanager.com/gtag/js?id=" + GA_ID + "');",
    ]
    if with_ads:
        lines.append("      load('https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + AD_CLIENT + "', true);")
    lines += ["    })();", "  </script>"]
    return nl.join(lines) + nl


def main():
    changed, skipped, unmatched = [], [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, ROOT).replace("\\", "/")
            with open(fp, "r", encoding="utf-8", errors="ignore", newline="") as fh:
                src = fh.read()
            if MARKER in src or "gtag/js" not in src:
                continue
            if EXCLUDE and EXCLUDE.search(rel):
                skipped.append(rel)
                continue
            ga = GA_RE.search(src)
            ads = AD_RE.findall(src)
            if not ga or len(ads) > 1:
                unmatched.append(rel)
                continue
            nl = "\r\n" if "\r\n" in src else "\n"
            out = src[:ga.start()] + guard(bool(ads), nl) + src[ga.end():]
            out = AD_RE.sub("", out, count=1)
            if "gtag/js?id=" + GA_ID + '"' in out or 'adsbygoogle.js?client=' + AD_CLIENT + '" crossorigin' in out:
                unmatched.append(rel)
                continue
            changed.append(rel)
            if not DRY_RUN:
                with open(fp, "w", encoding="utf-8", newline="") as fh:
                    fh.write(out)

    print(("Would change" if DRY_RUN else "Changed") + f" {len(changed)} page(s).")
    if skipped:
        print(f"Skipped {len(skipped)} excluded page(s).")
    if unmatched:
        print(f"Left {len(unmatched)} page(s) with a loader this script doesn't recognise:")
        for r in unmatched:
            print("  " + r)
    return 1 if unmatched else 0


if __name__ == "__main__":
    sys.exit(main())
