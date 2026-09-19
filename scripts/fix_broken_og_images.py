"""
audit_og_images.py found every og:image/twitter:image URL that 404s.
Two categories:

1. assets/images/app_logo.png -- referenced by 430 og:image/twitter:image
   tags across 225 pages (including the homepage) -- never existed in
   this repo at all (confirmed via `git log --all`, zero history). Every
   one of those pages has been showing NO image preview in search results
   or social shares this entire time. Repointed to app_icon_512.png,
   which is real, 512x512, and already used as the PWA icon.

2. assets/images/vegetables/bell-pepper.png -- a hyphen/space mismatch;
   the real file is "bell pepper.png". Fixed to match (percent-encoded,
   consistent with how the site's other space-containing filenames like
   scientists' portraits are already referenced elsewhere).

3. ~28 other unique preview/collage/cover images (vegetables-preview.jpg,
   alphabets/alphabet-collection.png, etc.) were apparently planned but
   never actually created/uploaded -- there's no existing substitute
   asset to point to instead, so these also fall back to
   app_icon_512.png rather than continuing to 404. Custom per-page
   preview art for these ~28 pages is a content task, not something this
   script invents.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
DRY_RUN = "--dry-run" in sys.argv

FALLBACK = "app_icon_512.png"

REPLACEMENTS = {
    "assets/images/app_logo.png": f"assets/images/{FALLBACK}",
    "assets/images/vegetables/bell-pepper.png": "assets/images/vegetables/bell%20pepper.png",
    "assets/images/vegetables-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/images/alphabets-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/images/countries-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/images/worksheet-cover.png": f"assets/images/{FALLBACK}",
    "assets/images/electronic-gadgets-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/images/fantasy-characters-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/images/alphabets/alphabet-collection.png": f"assets/images/{FALLBACK}",
    "assets/images/animals/animal-collection.png": f"assets/images/{FALLBACK}",
    "assets/images/birds/bird-collection.png": f"assets/images/{FALLBACK}",
    "assets/images/bodyparts/body-collection.png": f"assets/images/{FALLBACK}",
    "assets/images/colors/rainbow-collage.jpg": f"assets/images/{FALLBACK}",
    "assets/images/country/world-map-collage.jpg": f"assets/images/{FALLBACK}",
    "assets/images/electronics/tech-collage.jpg": f"assets/images/{FALLBACK}",
    "assets/images/fruits/fruit-basket-collage.jpg": f"assets/images/{FALLBACK}",
    "assets/images/learning-hub-banner.jpg": f"assets/images/{FALLBACK}",
    "assets/images/planets/solar-system-collage.jpg": f"assets/images/{FALLBACK}",
    "assets/images/vegetables/veggie-basket-collage.jpg": f"assets/images/{FALLBACK}",
    "assets/images/vehicles/vehicle-collage.jpg": f"assets/images/{FALLBACK}",
    "assets/images/odd-even-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/images/planets-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/images/plants-cover.png": f"assets/images/{FALLBACK}",
    "assets/images/publicservice-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/images/rhyming-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/images/scientists-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/cover/shapes-cover.png": f"assets/images/{FALLBACK}",
    "assets/images/sight-words-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/images/vehicles-preview.jpg": f"assets/images/{FALLBACK}",
    "assets/images/word-matching-preview.jpg": f"assets/images/{FALLBACK}",
}


def main():
    total_replacements = 0
    changed = []

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            original = content
            file_replacements = 0
            for broken, fixed in REPLACEMENTS.items():
                if broken in content:
                    n = content.count(broken)
                    content = content.replace(broken, fixed)
                    file_replacements += n
            if content != original:
                total_replacements += file_replacements
                rel = os.path.relpath(fp, ROOT).replace("\\", "/")
                changed.append((rel, file_replacements))
                if not DRY_RUN:
                    with open(fp, "w", encoding="utf-8", newline="") as fh:
                        fh.write(content)

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Pages changed: {len(changed)}")
    print(f"Total URL replacements: {total_replacements}")
    for f, n in changed[:10]:
        print(f"  {f}: {n}")
    if len(changed) > 10:
        print(f"  ... and {len(changed) - 10} more")


if __name__ == "__main__":
    main()
