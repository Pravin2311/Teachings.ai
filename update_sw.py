# update-sw.py (Debug Version)
import os
import re

# Paths
SERVICE_WORKER = "service-worker.js"
CSS_DIR = "css"
JS_DIR = "js"

print("🔍 Scanning files...")

# Collect URLs
urls = [
    '/',
    '/index.html',
    '/manifest.json'
]

# Add HTML pages
for file in os.listdir("."):
    if file.endswith(".html") and file != "service-worker.js":
        urls.append(f"/{file}")
        print(f"  ✅ HTML: {file}")

# Add CSS
if os.path.exists(CSS_DIR):
    for file in os.listdir(CSS_DIR):
        if file.endswith(".css"):
            urls.append(f"/css/{file}")
            print(f"  ✅ CSS: {file}")

# Add JS
if os.path.exists(JS_DIR):
    for file in os.listdir(JS_DIR):
        if file.endswith(".js") and "service-worker" not in file:
            urls.append(f"/js/{file}")
            print(f"  ✅ JS: {file}")

# Add key assets
assets = [
    '/assets/audio/background_music.mp3',
    '/assets/audio/click.mp3',
    '/assets/images/app_icon_192.png',
    '/assets/images/app_icon_512.png'
]
for asset in assets:
    urls.append(asset)
    print(f"  ✅ Asset: {asset}")

# Sort and deduplicate
urls = sorted(set(urls))
print(f"📦 Total URLs to cache: {len(urls)}")

# Read service-worker.js
try:
    with open(SERVICE_WORKER, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"📄 {SERVICE_WORKER} read successfully")
except FileNotFoundError:
    print(f"❌ Error: {SERVICE_WORKER} not found in current directory")
    exit(1)
except Exception as e:
    print(f"❌ Error reading file: {e}")
    exit(1)

# Flexible regex to match urlsToCache array
pattern = r"(const urlsToCache = \[\s*)(?:[\s\S]*?)(\]\s*;\s*//\s*Assets)"
match = re.search(pattern, content, re.IGNORECASE)

if not match:
    print("❌ FAILED: Regex did not match!")
    print("💡 Make sure you have this in service-worker.js:")
    print('const urlsToCache = [\n  // ... URLs\n]; // Assets')
    print("\n👉 Check the comment '// Assets' exists and is on the same line as '];'")
    exit(1)

print("✅ Regex matched! Replacing...")

# Build new list
urls_js = ",\n  ".join(f"'{url}'" for url in urls)
replacement = f"const urlsToCache = [\n  {urls_js}\n]; // Assets"

# Replace
updated_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

# Write back
try:
    with open(SERVICE_WORKER, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"✅ SUCCESS: {SERVICE_WORKER} updated with {len(urls)} URLs!")
    print("👉 Commit the changes in GitHub Desktop")
except Exception as e:
    print(f"❌ Error writing file: {e}")
    print("💡 Make sure the file isn't open in another program")