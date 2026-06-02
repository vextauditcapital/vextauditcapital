import re
import os

with open('../onboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for service definitions, mappings, or keys
# Common pattern might be a JS object or select options
print("--- Options in select or JS objects ---")
select_matches = re.findall(r'<option[^>]*value=["\']([^"\']+)["\'][^>]*>(.*?)</option>', content)
for m in select_matches:
    print(f"Option: {m[0]} -> {m[1].strip()}")

js_objects = re.findall(r'(\w+)\s*:\s*\{\s*name\s*:\s*["\']([^"\']+)["\']', content)
for m in js_objects:
    print(f"JS Object: {m[0]} -> {m[1]}")
