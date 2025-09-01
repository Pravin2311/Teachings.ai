# update-sw.py
import os
import re

# Paths
SERVICE_WORKER = "service-worker.js"
ROOT_DIR = "."
HTML_PAGES_DIR = "."  # All HTML files in root
CSS_DIR = "css"
JS_DIR = "js"
ASSETS_DIR = "assets"

# Collect files
urls = [
  '/',
  '/index.html',
  '/manifest.json'
]

# Add HTML pages (excluding service-worker.js and special files)
for file in os.listdir(HTML_PAGES_DIR):
    if file.endswith(".html") and file != "service-worker.js":
        urls.append(f'/{file}')

# Add CSS
for file in os.listdir(CSS_DIR):
    if file.endswith(".css"):
        urls.append(f'/css/{file}')

# Add JS
for file in os.listdir(JS_DIR):
    if file.endswith(".js") and "service-worker" not in file:
        urls.append(f'/js/{file}')

# Add key assets
assets = [
    '/assets/audio/background_music.mp3',
    '/assets/audio/click.mp3',
    '/assets/images/app_icon_192.png',
    '/assets/images/app_icon_512.png'
]
urls.extend(assets)

# Sort for consistency
urls = sorted(set(urls))

# Read service-worker.js
with open(SERVICE_WORKER, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace urlsToCache array
urls_js = ",\n  ".join(f"  '{url}'" for url in urls)
pattern = r"(const urlsToCache = \[)[^\]]*?(\];\s*// Assets)"
replacement = f"\\1\n  {urls_js}\n\\2"

updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open(SERVICE_WORKER, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print(f"✅ Updated {SERVICE_WORKER} with {len(urls)} files")
print("👉 Commit the changes!")