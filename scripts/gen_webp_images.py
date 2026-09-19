"""
Converts every PNG/JPG image under assets/images/ (above a size floor,
below which WebP's container overhead can make small files bigger, not
smaller) to a sibling .webp file at quality=82 -- visually
near-identical, real content images averaging 30-50% smaller in local
testing (a 61MB total image payload is a real Core Web Vitals cost).

Purely additive: originals are never touched or removed, so nothing
that currently works can break from this step alone. Skips a file if
its own WebP output would end up larger (true for some very small/flat
icons) or if a .webp already exists and is newer than the source.
"""
import os
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(ROOT, "assets", "images")
MIN_SIZE_BYTES = 3000  # below this, WebP overhead often isn't worth it
QUALITY = 82
DRY_RUN = "--dry-run" in sys.argv


def main():
    converted, skipped_small, skipped_bigger, skipped_uptodate, errors = 0, 0, 0, 0, 0
    total_before, total_after = 0, 0

    for dirpath, dirnames, filenames in os.walk(IMAGES_DIR):
        if os.path.basename(dirpath) == "og":
            continue  # branded OG cards already generated small/optimized
        for fn in filenames:
            if not fn.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            src_path = os.path.join(dirpath, fn)
            base, _ = os.path.splitext(src_path)
            webp_path = base + ".webp"

            src_size = os.path.getsize(src_path)
            if src_size < MIN_SIZE_BYTES:
                skipped_small += 1
                continue

            if os.path.isfile(webp_path) and os.path.getmtime(webp_path) >= os.path.getmtime(src_path):
                skipped_uptodate += 1
                continue

            try:
                im = Image.open(src_path)
                if im.mode in ("P", "LA") or (im.mode == "RGBA" and fn.lower().endswith((".jpg", ".jpeg"))):
                    im = im.convert("RGBA")
                if not DRY_RUN:
                    im.save(webp_path, "WEBP", quality=QUALITY, method=6)
                webp_size = os.path.getsize(webp_path) if not DRY_RUN else src_size  # estimate skipped in dry run
            except Exception as e:
                errors += 1
                print(f"ERROR converting {os.path.relpath(src_path, ROOT)}: {e}")
                continue

            if not DRY_RUN and webp_size >= src_size:
                os.remove(webp_path)
                skipped_bigger += 1
                continue

            converted += 1
            total_before += src_size
            total_after += webp_size if not DRY_RUN else src_size

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Converted: {converted}")
    print(f"Skipped (already up to date): {skipped_uptodate}")
    print(f"Skipped (below {MIN_SIZE_BYTES}-byte floor): {skipped_small}")
    print(f"Skipped (WebP would be bigger): {skipped_bigger}")
    print(f"Errors: {errors}")
    if total_before:
        print(f"Payload: {total_before/1024:.0f} KB -> {total_after/1024:.0f} KB "
              f"({100*total_after/total_before:.0f}%, saved {(total_before-total_after)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
