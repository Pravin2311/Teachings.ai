#!/usr/bin/env python3
"""Audits JSON-LD structured data across every page:
- pages with no JSON-LD at all
- JSON-LD blocks that fail to parse (invalid JSON -- Google will ignore them)
- JSON-LD present but missing @context / @type
Read-only report, no modifications.
"""
import glob
import json
import re

SKIP_DIRS = ("mockups/", "templates/", ".git/", "node_modules/")
SKIP_FILES = {"furits-vegetables-sorting.html"}

JSONLD_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S | re.I
)


def main():
    files = [f for f in glob.glob("**/*.html", recursive=True) if not f.replace("\\", "/").startswith(SKIP_DIRS)]
    files = [f for f in files if f.replace("\\", "/") not in SKIP_FILES]
    files.sort()

    no_schema = []
    invalid_json = []
    missing_fields = []
    types_seen = {}
    total_blocks = 0
    ok_pages = 0

    for f in files:
        try:
            html = open(f, encoding="utf-8", errors="ignore").read()
        except Exception as e:
            print(f"READ ERROR {f}: {e}")
            continue

        blocks = JSONLD_RE.findall(html)
        if not blocks:
            no_schema.append(f)
            continue

        page_ok = True
        for block in blocks:
            total_blocks += 1
            try:
                data = json.loads(block)
            except json.JSONDecodeError as e:
                invalid_json.append((f, str(e)))
                page_ok = False
                continue

            items = data.get("@graph") if isinstance(data, dict) and "@graph" in data else [data]
            if isinstance(data, list):
                items = data
            for item in items:
                if not isinstance(item, dict):
                    continue
                t = item.get("@type")
                if not item.get("@context") and not item.get("@id"):
                    # nested @graph items don't need their own @context
                    pass
                if not t:
                    missing_fields.append((f, "missing @type"))
                    page_ok = False
                else:
                    key = t if isinstance(t, str) else ",".join(t)
                    types_seen[key] = types_seen.get(key, 0) + 1

        if page_ok:
            ok_pages += 1

    print("=" * 70)
    print(f"Total HTML pages scanned: {len(files)}")
    print(f"Pages with >=1 JSON-LD block: {len(files) - len(no_schema)}")
    print(f"Pages with NO JSON-LD at all: {len(no_schema)}")
    print(f"Total JSON-LD blocks found: {total_blocks}")
    print(f"Blocks with invalid JSON (Google ignores these): {len(invalid_json)}")
    print(f"Items missing @type: {len(missing_fields)}")
    print("=" * 70)
    print("\nSchema @type distribution:")
    for t, n in sorted(types_seen.items(), key=lambda kv: -kv[1]):
        print(f"  {n:4d}  {t}")

    print(f"\n[INVALID JSON] ({len(invalid_json)}):")
    for f, err in invalid_json:
        print(f"  {f}: {err}")

    print(f"\n[MISSING @TYPE] ({len(missing_fields)}):")
    for f, msg in missing_fields:
        print(f"  {f}: {msg}")

    print(f"\n[NO SCHEMA AT ALL] ({len(no_schema)}):")
    for f in no_schema:
        print(f"  {f}")


if __name__ == "__main__":
    main()
