const API_KEY = "08432b78661d4e0c800e50116836496f";
const HOST = "www.teachings.ai"; // must match the host of the URLs in the sitemap
const SITEMAP_URL = "https://www.teachings.ai/sitemap.xml";

async function run() {
  console.log(`Fetching sitemap from ${SITEMAP_URL}...`);

  const sitemap = await fetch(SITEMAP_URL).then((r) => r.text());

  const urls = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map((m) => m[1]);

  console.log(`Found ${urls.length} URLs.`);

  if (urls.length === 0) {
    console.error("No URLs found in sitemap.");
    return;
  }

  const body = {
    host: HOST,
    key: API_KEY,
    urlList: urls,
  };

  const res = await fetch("https://api.indexnow.org/indexnow", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  console.log("HTTP Status:", res.status);

  if (res.ok) {
    console.log(`✅ Successfully submitted ${urls.length} URLs to IndexNow.`);
  } else {
    console.error("❌ Submission failed.");
    console.error(await res.text());
  }
}

run().catch(console.error);