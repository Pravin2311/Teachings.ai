# Weekly SEO workflow

`seo/weekly.py` fetches the latest complete Search Console, GA4 and AdSense data
(read-only), saves a dated snapshot, evaluates the experiments in
`experiments.json`, and writes a dated report plus a prioritized plan.

| Path | In git? | What |
|---|---|---|
| `gapi.py`, `weekly.py`, `analysis.py`, `config.json`, `requirements.txt`, `run_weekly.cmd` | yes | code and settings (no secrets) |
| `experiments.json` | yes | experiment log: hypothesis, change, date, metric, evaluations |
| `data/YYYY-MM-DD/` | **no** | raw API snapshots |
| `reports/YYYY-MM-DD.md` + `-plan.json` | **no** | weekly reports (contain revenue; the repo is public) |
| `%APPDATA%\teachings-seo\` | **no** (outside the repo) | OAuth client file and token |

`seo/` is also in `.vercelignore`, so none of it is deployed.

Nothing in this folder writes to Google, the site, ads or DNS. It never commits or deploys anything.

## One-time setup (about 15 minutes, all in your browser)

Why OAuth and not a service account: the AdSense Management API does not support
service accounts, and one OAuth desktop client covers all three APIs with a single consent.
All three scopes are read-only:
`webmasters.readonly`, `analytics.readonly`, `adsense.readonly`.

1. **Create a Google Cloud project.** Go to <https://console.cloud.google.com/projectcreate>
   and create a project, for example `teachings-seo`. No billing is needed.

2. **Enable four APIs** in that project. Open each link and click **Enable**:
   - Search Console API: <https://console.cloud.google.com/apis/library/searchconsole.googleapis.com>
   - Google Analytics Data API: <https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com>
   - Google Analytics Admin API (only used to find the GA4 property id): <https://console.cloud.google.com/apis/library/analyticsadmin.googleapis.com>
   - AdSense Management API: <https://console.cloud.google.com/apis/library/adsense.googleapis.com>

3. **Configure the OAuth consent screen and create a desktop client.**
   - Go to <https://console.cloud.google.com/auth/overview> and click **Get started**.
     Enter an app name (for example `teachings-seo`) and your email, choose **External** as the audience,
     and finish.
   - Under **Audience**, click **Publish app** so the app status is **In production**.
     *Why:* in "Testing" status Google expires refresh tokens after 7 days, which would break the weekly run.
     You don't need Google verification for your own use. On first sign-in you'll see
     "Google hasn't verified this app". Click **Advanced**, then **Go to teachings-seo**.
   - Under **Clients**, click **Create client**, choose **Desktop app**, then **Create**, and **Download JSON**.
   - Move the downloaded `client_secret_….json` file into `%APPDATA%\teachings-seo\`
     (that is `C:\Users\whynew\AppData\Roaming\teachings-seo\`). You don't need to rename it.
     Don't put it in the repo or paste it into chat.

4. **Sign in once** (opens a browser; use the Google account that owns Search Console, GA4 and AdSense):
   ```
   seo\.venv\Scripts\python seo\weekly.py --auth
   ```
   The token is saved next to the client file. To revoke access at any time, go to
   <https://myaccount.google.com/permissions>.

5. **Test against real data:**
   ```
   seo\.venv\Scripts\python seo\weekly.py --check
   ```
   Each source prints `[ ok ]` with real numbers, or `[FAIL]` with what to fix.
   The script auto-detects the Search Console property (`sc-domain:teachings.ai` or the URL-prefix
   property) and finds the GA4 property whose web stream has measurement id `G-XVYMNTZLQJ`.
   To pin either one, set `gsc_site` / `ga4_property_id` in `config.json`.

6. **Optional, for page-level ad revenue:** link AdSense to GA4
   (GA4 **Admin → Product links → AdSense links**). Until that link exists, GA4 can't report revenue
   per page. The report says so and still shows account-level earnings and RPM from the AdSense API.
   This changes account settings, so it's your call.

7. **Bing Webmaster Tools** (Bing and Yahoo send most of the site's organic users, and Search Console
   doesn't see them). See <https://learn.microsoft.com/en-us/bingwebmaster/getting-access>.
   - Sign in at <https://www.bing.com/webmasters>. If `teachings.ai` isn't there yet, add it. The quickest way is
     **Import from Google Search Console**, which verifies it using your existing Google verification.
   - Click **Settings** (top right), then **API Access**. Accept the terms, then click **API Key** and **Generate API Key**.
   - Save only the key, on one line, in `%APPDATA%\teachings-seo\bing_api_key.txt`
     (that is `C:\Users\whynew\AppData\Roaming\teachings-seo\bing_api_key.txt`). Don't paste it into chat or the repo.
   - Run `--check` again. You should see a `[ ok ] Bing ...` line.
   The key belongs to your Bing user, not a site, so it also reaches any other sites in that account. The script
   only calls read-only `Get*` methods. If the key leaks, delete it and generate a new one on the same page.

If the venv is missing (new machine):
```
python -m venv seo\.venv
seo\.venv\Scripts\pip install -r seo\requirements.txt
```

## Weekly run

```
seo\.venv\Scripts\python seo\weekly.py
```
Writes `seo/reports/<today>.md`, `seo/reports/<today>-plan.json` and `seo/data/<today>/snapshot-api.json`,
and appends interim or final evaluations to `experiments.json`.

Without the API (for example, before setup), build the report from a Search Console UI export
(Performance → Export → Excel):
```
seo\.venv\Scripts\python seo\weekly.py --from-export path\to\teachings.ai-Performance-on-Search-YYYY-MM-DD.xlsx
```

### Scheduling (Windows Task Scheduler)

Runs every Monday at 09:00 while you're logged in. Output goes to `seo\logs\weekly.log`:
```
schtasks /Create /TN "TeachingsSEO-Weekly" /SC WEEKLY /D MON /ST 09:00 /TR "\"C:\Users\whynew\Documents\GitHub\Teachings.ai\seo\run_weekly.cmd\""
schtasks /Run /TN "TeachingsSEO-Weekly"      # test it now
schtasks /Query /TN "TeachingsSEO-Weekly" /V /FO LIST
schtasks /Delete /TN "TeachingsSEO-Weekly" /F # remove it
```
If the PC is off at 09:00 Monday, that week is skipped. To run the missed task when the PC
next starts, open Task Scheduler → task → Properties → Settings and tick
**"Run task as soon as possible after a scheduled start is missed"**.
Check `seo\logs\weekly.log` (or the newest file in `seo\reports\`) before relying on a run.

## The learning loop

1. Before a meaningful change ships, add an entry to `experiments.json`: `id`, `date` (deploy date),
   `pages_regex` (a regex on the URL), `change`, `hypothesis`, `metric`, `window_days`,
   `evaluate_after` (deploy date plus at least 4 weeks), `status: "running"`.
2. Each weekly run records the pre-change baseline, then compares the experiment pages after the change
   with the **rest of the site over the same days** (a control for site-wide and seasonal swings).
   Verdicts stay "interim" until `evaluate_after` has passed and there are at least 30 clicks.
   For changes aimed at what visitors do after landing (not at search), add
   `"ga4_engagement": {"control_regex": "..."}`. The report then also compares GA4 organic sessions landing on
   the experiment pages with sessions landing on the control pages: views per session (descriptive) and engaged
   rate (with a z-score). It needs at least 50 sessions per group and window. GA4 has no "sessions with 2+ pages"
   metric, so views per session stands in for it.
   Every experiment also gets the same before/after comparison on **Bing page stats**. These are weekly buckets,
   and buckets dated within 7 days of the change are skipped. Set `"primary_source": "bing"` when most of the
   pages' search traffic comes from Bing; the verdict then uses Bing clicks (needs 30+) instead of Search Console.
3. Pages inside a running experiment are held back from new recommendations, so the experiment
   stays readable. For performance-only changes (caching, image loading), set `"holds_back": false`.
   Otherwise a site-wide experiment would freeze every page for a month.
4. When an experiment is evaluated, set `status` to `kept`, `revised` or `reverted` and write the
   `next_action`. A good result is evidence, not proof that the change caused it.

The report checks whether last week's tasks were implemented by looking for git commits that touch
each page since the plan date. That shows whether the page changed, not whether the change was good.

## Limits

- Search Console data lags 2–3 days, so the run ends 3 days ago (`gsc_lag_days`).
- The "estimated extra clicks" column uses the rough CTR-by-position assumptions in `config.json`.
  They're planning guesses, not benchmarks, and only rank work. Replace them with the site's own
  CTR curve once there's enough click data.
- At the current volume (a few clicks a day), most page-level changes can't be told apart from noise
  for weeks. Impressions and position move first.
