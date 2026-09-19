"""
CRITICAL: every previous audit this session used os.path.isfile(), which
is case-INSENSITIVE on this Windows dev machine -- so a reference to
"canada.png" was silently treated as "exists" when the real file is
"Canada.png". GitHub Pages serves from case-SENSITIVE Linux storage, so
any such mismatch is a live 404 in production that every earlier audit
this session would have missed entirely.

This checks every local asset reference (img src, link href, script src,
audio/video src) against the real, case-exact directory listing, and
reports any reference that only "works" because of case-insensitive
matching.
"""
import os
import re
from urllib.parse import unquote
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"mockups", "templates", ".git", "node_modules"}
CDN_PREFIX = "https://cdn.jsdelivr.net/gh/Pravin2311/Teachings.ai@main/"

REF_RE = re.compile(
    r'\b(?:src|href)="([^"]+)"',
    re.IGNORECASE,
)

# build a case-exact index of every real file, keyed by lowercased relpath.
# NOTE: deliberately NOT using os.path.isfile() as the "does this exact
# reference exist" check anywhere below -- it's case-INSENSITIVE on this
# Windows machine, which would defeat the entire point of this script.
_real_files_exact = set()
_real_files_lower = {}
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
    for fn in filenames:
        rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/")
        _real_files_exact.add(rel)
        _real_files_lower[rel.lower()] = rel


def resolve(ref, source_file):
    if "${" in ref or ref.startswith("data:") or ref.startswith("#") or ref.startswith("mailto:") \
       or ref.startswith("javascript:") or ref.startswith("tel:"):
        return None
    if ref.startswith(CDN_PREFIX):
        rel = ref[len(CDN_PREFIX):]
    elif ref.startswith("http://") or ref.startswith("https://"):
        return None
    elif ref.startswith("/"):
        rel = ref.lstrip("/")
    else:
        source_dir = os.path.dirname(source_file)
        rel = os.path.normpath(os.path.join(source_dir, ref)).replace("\\", "/")
    rel = rel.split("#")[0].split("?")[0]
    return unquote(rel)


def main():
    mismatches = defaultdict(list)
    truly_missing = defaultdict(list)
    checked = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith((".html", ".css")):
                continue
            fp = os.path.join(dirpath, fn)
            rel_file = os.path.relpath(fp, ROOT).replace("\\", "/")
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            for m in REF_RE.finditer(content):
                ref = m.group(1)
                target = resolve(ref, rel_file)
                if target is None or not target:
                    continue
                checked += 1
                if target in _real_files_exact:
                    continue  # exact case match -- genuinely fine
                real = _real_files_lower.get(target.lower())
                if real:
                    mismatches[(target, real)].append(rel_file)
                else:
                    truly_missing[target].append(rel_file)

    print(f"References checked: {checked}")
    print(f"CASE-MISMATCH (works locally on Windows, WILL 404 on GitHub Pages): {len(mismatches)}")
    print(f"Truly missing (no file at any case): {len(truly_missing)}")
    print()
    print("=== CASE MISMATCHES ===")
    for (referenced, real), pages in sorted(mismatches.items()):
        print(f"  referenced: {referenced}")
        print(f"  real file:  {real}")
        for p in sorted(set(pages))[:5]:
            print(f"    used in {p}")
        print()

    print("=== TRULY MISSING (no file at any case) ===")
    for target, pages in sorted(truly_missing.items()):
        print(f"  {target}  ({len(set(pages))} pages)")
        for p in sorted(set(pages))[:3]:
            print(f"    used in {p}")


if __name__ == "__main__":
    main()
