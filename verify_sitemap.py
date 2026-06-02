import os
import xml.etree.ElementTree as ET

sitemap_path = r"C:\Users\shyam\.gemini\antigravity\scratch\sitemap.xml"
dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"

print("=== START SITEMAP INTEGRITY AUDIT ===")

if not os.path.exists(sitemap_path):
    print(f"Error: Sitemap not found at {sitemap_path}")
    exit(1)

# Parse sitemap
try:
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
except Exception as e:
    print(f"Error parsing sitemap.xml: {e}")
    exit(1)

# Namespaces in sitemap.xml
namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

sitemap_urls = []
for url_elem in root.findall('ns:url', namespaces):
    loc_elem = url_elem.find('ns:loc', namespaces)
    if loc_elem is not None:
        sitemap_urls.append(loc_elem.text)

print(f"Sitemap contains {len(sitemap_urls)} URLs.")

# Verify each URL exists locally
missing_files = []
local_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

for url in sitemap_urls:
    # Extract filename from URL (e.g., https://www.vextaudit.com/about.html -> about.html)
    filename = url.replace("https://www.vextaudit.com/", "").replace("https://vextaudit.com/", "")
    
    # Handle root URL (e.g. index.html)
    if not filename or filename == "/":
        filename = "index.html"
        
    local_filepath = os.path.join(dir_path, filename)
    if not os.path.exists(local_filepath):
        missing_files.append((url, filename))
    else:
        print(f"Verified: {filename} exists and is matched in sitemap.")

print("\n=== AUDIT RESULTS ===")
if missing_files:
    print(f"WARNING: {len(missing_files)} URLs in sitemap do not match any local HTML file:")
    for url, fn in missing_files:
        print(f"  - Loc: {url} (expected local file: {fn})")
else:
    print("SUCCESS: All URLs listed in sitemap.xml correspond to actual active local HTML files. Sitemap is 100% verified!")
