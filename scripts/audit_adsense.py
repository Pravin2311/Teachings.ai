#!/usr/bin/env python3
"""Audits every HTML page for AdSense-policy risk signals:
- ad unit count per page
- adjacent/stacked ad units (no real content between them)
- thin content relative to ad count (ads on low-word-count pages)
- wrong/missing publisher ID on any ad unit
- malformed ad units (missing data-ad-slot)
Does not modify anything -- read-only report.
"""
import glob
import re

EXPECTED_CLIENT = "ca-pub-7495143337429327"
THIN_CONTENT_WORDS = 150  # pages with ads and fewer visible words than this get flagged

SKIP_DIRS = ("mockups/", ".git/", "node_modules/")


def visible_word_count(html):
    # Strip script/style blocks entirely (not real page content)
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    # Strip all remaining tags
    text = re.sub(r"<[^>]+>", " ", html)
    words = re.findall(r"[A-Za-z0-9']+", text)
    return len(words)


def find_ad_blocks(html):
    """Return list of (start_index, end_index) for each <ins class="adsbygoogle">...</ins> block."""
    return [m.span() for m in re.finditer(r"<ins\s+class=\"adsbygoogle\"[^>]*>.*?</ins>", html, re.S)]


def main():
    files = [f for f in glob.glob("**/*.html", recursive=True) if not f.startswith(SKIP_DIRS)]
    files.sort()

    total_pages = 0
    pages_with_ads = 0
    flagged_stacked = []
    flagged_thin = []
    flagged_bad_client = []
    flagged_malformed = []
    flagged_high_count = []
    ad_count_hist = {}

    for f in files:
        try:
            html = open(f, encoding="utf-8", errors="ignore").read()
        except Exception as e:
            print(f"READ ERROR {f}: {e}")
            continue
        total_pages += 1

        ad_blocks = find_ad_blocks(html)
        n_ads = len(ad_blocks)
        ad_count_hist[n_ads] = ad_count_hist.get(n_ads, 0) + 1
        if n_ads == 0:
            continue
        pages_with_ads += 1

        if n_ads >= 3:
            flagged_high_count.append((f, n_ads))

        # Check each ad block for correct client + slot present
        for start, end in ad_blocks:
            block = html[start:end]
            if EXPECTED_CLIENT not in block:
                flagged_bad_client.append(f)
            if "data-ad-slot" not in block and "data-ad-client" not in block:
                flagged_malformed.append(f)

        # Check for stacked/adjacent ad blocks (less than ~40 non-tag chars between them)
        for i in range(len(ad_blocks) - 1):
            gap_start = ad_blocks[i][1]
            gap_end = ad_blocks[i + 1][0]
            gap_html = html[gap_start:gap_end]
            gap_text = re.sub(r"<[^>]+>", "", gap_html).strip()
            if len(gap_text) < 40:
                flagged_stacked.append((f, len(gap_text)))

        # Thin content check
        wc = visible_word_count(html)
        if wc < THIN_CONTENT_WORDS:
            flagged_thin.append((f, wc, n_ads))

    print("=" * 70)
    print(f"Total HTML pages scanned: {total_pages}")
    print(f"Pages with >=1 ad unit:   {pages_with_ads}")
    print(f"Ad-count distribution:    {dict(sorted(ad_count_hist.items()))}")
    print("=" * 70)

    print(f"\n[HIGH COUNT] Pages with 3+ ad units ({len(flagged_high_count)}):")
    for f, n in flagged_high_count:
        print(f"  {f}: {n} ads")

    print(f"\n[STACKED] Ad units with <40 chars of real content between them ({len(flagged_stacked)}):")
    for f, gap in flagged_stacked:
        print(f"  {f}: gap={gap} chars")

    print(f"\n[THIN CONTENT] Pages with ads but <{THIN_CONTENT_WORDS} visible words ({len(flagged_thin)}):")
    for f, wc, n in flagged_thin:
        print(f"  {f}: {wc} words, {n} ad(s)")

    print(f"\n[BAD CLIENT ID] Ad blocks missing/wrong publisher ID ({len(flagged_bad_client)}):")
    for f in sorted(set(flagged_bad_client)):
        print(f"  {f}")

    print(f"\n[MALFORMED] Ad blocks missing data-ad-slot/data-ad-client ({len(flagged_malformed)}):")
    for f in sorted(set(flagged_malformed)):
        print(f"  {f}")


if __name__ == "__main__":
    main()
