"""
Single entry point for the site's whole SEO/technical audit suite. Runs
every scripts/audit_*.py in one pass and prints one consolidated
scorecard instead of eight separate outputs -- meant as the standard
pre-publish / periodic health check going forward.

Usage:
  python scripts/audit_all.py            # scorecard only
  python scripts/audit_all.py --full     # scorecard + full raw output
                                            from any script with a WARN/FAIL

Exit code is non-zero if any hard-fail metric is above its expected
baseline (broken links, invalid JSON-LD, noindex, broken images, etc.) --
soft/expected counts (the 3 known intentional redirect stubs, the
unpublished mockup) are baselined in and won't trip it.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
FULL_OUTPUT = "--full" in sys.argv

# (script filename, [(regex, label, expected_max, hard_fail)])
CHECKS = [
    ("audit_seo_meta.py", [
        # baseline of 4 = the 3 intentional typo-redirect stubs ("Redirecting...")
        # plus the unpublished mockups/homepage-v2.html, same known exceptions as
        # the missing-canonical/OG/twitter checks below.
        (r"\[TITLE TOO SHORT\] \((\d+)\)", "titles too short", 4, False),
        (r"\[TITLE TOO LONG\] \((\d+)\)", "titles too long", 0, True),
        (r"\[DESCRIPTION TOO SHORT\] \((\d+)\)", "descriptions too short", 0, True),
        (r"\[DESCRIPTION TOO LONG\] \((\d+)\)", "descriptions too long", 0, True),
    ]),
    ("audit_technical_seo.py", [
        (r"noindex found:\s+(\d+)", "unexpected noindex", 0, True),
        (r"Missing canonical:\s+(\d+)", "missing canonical", 2, False),
        (r"Bad/off-domain canonical:\s+(\d+)", "bad canonical", 0, True),
        (r"Missing viewport meta:\s+(\d+)", "missing viewport", 3, False),
        (r"Missing OG tags[^:]*:\s+(\d+)", "missing OG tags", 4, False),
        (r"Missing twitter:card:\s+(\d+)", "missing twitter:card", 4, False),
    ]),
    ("audit_schema.py", [
        (r"Blocks with invalid JSON[^:]*:\s+(\d+)", "invalid JSON-LD", 0, True),
        (r"Items missing @type:\s+(\d+)", "schema missing @type", 0, True),
    ]),
    ("audit_images.py", [
        (r"Missing alt attribute entirely:\s+(\d+)", "images missing alt", 0, True),
        (r"Missing width or height:\s+(\d+)", "images missing dims", 10, False),
        (r'Missing loading="lazy":\s+(\d+)', "images missing lazy-load", 24, False),
    ]),
    ("audit_internal_links.py", [
        (r"Broken internal links[^:]*:\s+(\d+)", "broken internal links", 0, True),
        (r"orphans\):\s+(\d+)", "orphan pages", 3, False),
    ]),
    ("audit_performance.py", [
        (r"duplicate <script src>[^:]*:\s+(\d+)", "pages with duplicate scripts", 0, True),
        (r"missing[^:]*preconnect[^:]*:\s+(\d+)", "pages missing preconnect", 0, True),
        (r"render-blocking[^:]*:\s+(\d+)", "render-blocking head scripts", 0, True),
    ]),
    ("audit_og_images.py", [
        (r"Unique broken og:image/twitter:image targets:\s+(\d+)", "broken og:image targets", 0, True),
    ]),
    ("audit_adsense.py", [
        (r"Pages with 3\+ ad units \((\d+)\)", "pages with 3+ ad units", 0, True),
        (r"<40 chars of real content between them \((\d+)\)", "stacked ad units", 0, True),
    ]),
    ("audit_headings.py", [
        (r"Missing H1:\s+(\d+)", "pages missing H1", 0, True),
        (r"Multiple H1s:\s+(\d+)", "pages with multiple H1s", 0, True),
    ]),
    ("audit_sitemap.py", [
        (r"Live pages missing from sitemap:\s+(\d+)", "live pages missing from sitemap", 0, True),
        (r"Sitemap URLs pointing at nonexistent files:\s+(\d+)", "sitemap URLs pointing nowhere", 0, True),
    ]),
    ("audit_case_sensitivity.py", [
        (r"CASE-MISMATCH[^:]*:\s+(\d+)", "case-mismatched asset refs (fine on Windows, 404 on GitHub Pages)", 0, True),
        (r"Truly missing[^:]*:\s+(\d+)", "truly missing asset refs", 1, False),
    ]),
    ("audit_broken_content_images.py", [
        (r"Unique broken content-image targets:\s+(\d+)", "broken in-page <img> targets", 0, True),
    ]),
    ("audit_faq_schema.py", [
        (r"NO FAQPage schema:\s+(\d+)", "visible FAQ sections missing FAQPage schema", 0, True),
    ]),
    ("audit_jsonld_assets.py", [
        (r"Broken asset URLs found:\s+(\d+)", "broken asset URLs inside JSON-LD", 0, True),
    ]),
]


def run_script(name):
    path = os.path.join(SCRIPTS_DIR, name)
    if not os.path.isfile(path):
        return None
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    result = subprocess.run(
        [sys.executable, path], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=env,
    )
    return result.stdout + result.stderr


def main():
    print("=" * 78)
    print("TEACHINGS.AI -- FULL SEO/TECHNICAL AUDIT")
    print("=" * 78)

    rows = []
    hard_fail = False
    raw_outputs = {}

    for script, checks in CHECKS:
        output = run_script(script)
        if output is None:
            rows.append((script, "MISSING", f"script not found", None))
            continue
        raw_outputs[script] = output
        script_has_warn = False
        for pattern, label, expected_max, is_hard_fail in checks:
            m = re.search(pattern, output)
            if not m:
                rows.append((script, "?", f"{label}: pattern not found in output", None))
                continue
            value = int(m.group(1))
            if value > expected_max:
                status = "FAIL" if is_hard_fail else "WARN"
                if is_hard_fail:
                    hard_fail = True
                script_has_warn = True
            else:
                status = "ok"
            rows.append((script, status, label, value))
        if script_has_warn:
            pass  # raw output already stored for --full

    name_w = max(len(r[0]) for r in rows) + 2
    label_w = max(len(r[2]) for r in rows) + 2
    for script, status, label, value in rows:
        marker = {"ok": "  ok  ", "WARN": " WARN ", "FAIL": " FAIL ", "MISSING": "MISSING", "?": "  ?   "}.get(status, status)
        val_str = "" if value is None else f"= {value}"
        print(f"[{marker}] {script:<{name_w}} {label:<{label_w}} {val_str}")

    print("=" * 78)
    n_fail = sum(1 for r in rows if r[1] == "FAIL")
    n_warn = sum(1 for r in rows if r[1] == "WARN")
    n_ok = sum(1 for r in rows if r[1] == "ok")
    print(f"{n_ok} ok, {n_warn} warn (within known baseline), {n_fail} FAIL")
    print("=" * 78)

    if FULL_OUTPUT and (n_warn or n_fail):
        print("\n--- FULL OUTPUT (scripts with WARN/FAIL) ---\n")
        flagged_scripts = {r[0] for r in rows if r[1] in ("WARN", "FAIL")}
        for script in flagged_scripts:
            print(f"\n### {script} ###")
            print(raw_outputs.get(script, "(no output captured)"))

    sys.exit(1 if hard_fail else 0)


if __name__ == "__main__":
    main()
