"""
Wires the WebP files gen_webp_images.py generated into the actual pages:
wraps each qualifying <img> in <picture><source type="image/webp">...
before it, leaving the original <img> tag byte-for-byte unchanged as
the fallback. This is the safe pattern -- any browser without WebP
support (or if a .webp is ever missing) silently falls through to the
exact same <img> that was already there; nothing about the existing
img (its id, class, JS hooks, alt, dimensions) changes at all.

Only targets <img src="/assets/images/...> or src="assets/images/...">
(local, resolvable paths) where a same-basename .webp file exists.
Skips: images already inside a <picture> (avoid double-wrapping), CDN-
prefixed src (jsdelivr mirrors this repo but its cache lags a commit,
so wiring those separately after the CDN catches up is safer), and JS
template-literal src (can't resolve statically).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
DRY_RUN = "--dry-run" in sys.argv

IMG_TAG_RE = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
SRC_RE = re.compile(r'\bsrc="([^"]+)"')
PICTURE_OPEN_BEFORE_RE = re.compile(r'<picture\b', re.IGNORECASE)


def resolve_local(src, source_file):
    if src.startswith("http://") or src.startswith("https://") or "${" in src or src.startswith("data:"):
        return None
    if src.startswith("/"):
        rel = src.lstrip("/")
    else:
        source_dir = os.path.dirname(source_file)
        rel = os.path.normpath(os.path.join(source_dir, src)).replace("\\", "/")
    return rel


def already_in_picture(content, tag_start):
    # look back up to 200 chars for an unclosed <picture> immediately before this img
    window = content[max(0, tag_start - 200):tag_start]
    return "<picture" in window and "</picture>" not in window


def main():
    total_wrapped = 0
    changed_files = []

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            rel_file = os.path.relpath(fp, ROOT).replace("\\", "/")
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()

            if 'http-equiv="refresh"' in content[:500]:
                continue

            matches = list(IMG_TAG_RE.finditer(content))
            if not matches:
                continue

            new_content = content
            offset = 0
            file_wrapped = 0
            for m in matches:
                tag = m.group(0)
                sm = SRC_RE.search(tag)
                if not sm:
                    continue
                src = sm.group(1)
                if not src.lower().endswith((".png", ".jpg", ".jpeg")):
                    continue
                rel_target = resolve_local(src, rel_file)
                if rel_target is None:
                    continue
                webp_rel = os.path.splitext(rel_target)[0] + ".webp"
                if not os.path.isfile(os.path.join(ROOT, webp_rel)):
                    continue
                if already_in_picture(content, m.start()):
                    continue

                webp_src = os.path.splitext(src)[0] + ".webp"
                replacement = f'<picture><source srcset="{webp_src}" type="image/webp">{tag}</picture>'

                start = m.start() + offset
                end = m.end() + offset
                new_content = new_content[:start] + replacement + new_content[end:]
                offset += len(replacement) - len(tag)
                file_wrapped += 1

            if file_wrapped:
                total_wrapped += file_wrapped
                changed_files.append((rel_file, file_wrapped))
                if not DRY_RUN:
                    with open(fp, "w", encoding="utf-8", newline="") as fh:
                        fh.write(new_content)

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Files changed: {len(changed_files)}")
    print(f"Total <img> wrapped in <picture>+WebP: {total_wrapped}")
    for rel, n in changed_files[:15]:
        print(f"  {rel}: +{n}")
    if len(changed_files) > 15:
        print(f"  ... and {len(changed_files) - 15} more")


if __name__ == "__main__":
    main()
