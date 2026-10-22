"""
URL-inspects every sitemap URL through the Search Console API (read-only)
and saves the coverage state, last crawl and canonicals per URL.

Usage:
  seo\\.venv\\Scripts\\python seo\\inspect_all.py [--limit N]

Writes seo/data/<today>/inspections-all.json. Quota: 2,000 inspections per
day per property (600/minute); the weekly run uses ~40, so don't run this
more than once a day.
"""
import datetime as dt
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gapi  # noqa: E402
import weekly  # noqa: E402


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    cfg = weekly.load_config()
    gsc = gapi.SearchConsole(gapi.get_credentials())
    site = weekly.pick_gsc_site(gsc, cfg)
    urls = weekly.sitemap_urls()[:limit]
    out_dir = os.path.join(weekly.DATA_DIR, dt.date.today().isoformat())
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "inspections-all.json")
    results = []
    for i, u in enumerate(urls, 1):
        for attempt in range(3):
            try:
                results.append(gsc.inspect(site, u))
                break
            except gapi.HttpError as e:
                if getattr(e.resp, "status", None) == 429 and attempt < 2:
                    time.sleep(60)  # per-minute quota; wait and retry
                    continue
                results.append({"url": u, "error": gapi.explain_http_error(e)})
                break
        time.sleep(0.15)
        if i % 50 == 0:
            print(f"{i}/{len(urls)}", flush=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=1)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
    print(f"Done: {len(results)} URLs -> {path}")


if __name__ == "__main__":
    main()
