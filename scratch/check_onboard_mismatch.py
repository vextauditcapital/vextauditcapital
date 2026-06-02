import re

path = r"C:\Users\shyam\.gemini\antigravity\scratch\onboard.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all cards: <div class="sc" data-svc="..." data-amt="..." data-lnk="...">
cards = re.findall(r'data-svc=["\']([^"\']+)["\']', content)
print(f"Cards found in onboard.html ({len(cards)}):")
for c in cards:
    print(f"  - {c}")

# Extract map entries inside javascript
# Let's search for the map definition block
map_match = re.search(r'var map\s*=\s*\{(.*?)\};', content, re.DOTALL)
if map_match:
    map_str = map_match.group(1)
    # find lines like: gst:['GST Audit & Compliance','25000','https://rzp.io/rzp/c8fadz3e'],
    entries = re.findall(r'[\'"]?(\w+[\-\w]*)[\'"]?\s*:\s*\[\s*[\'"]([^\'"]+)[\'"]', map_str)
    print(f"\nMap entries found ({len(entries)}):")
    map_dict = {}
    for k, v in entries:
        print(f"  - {k} => {v}")
        map_dict[k] = v
        
    print("\nVerifying if every map service name exists in card data-svc:")
    for k, v in map_dict.items():
        if v not in cards:
            print(f"  ❌ MISMATCH: Map key '{k}' has name '{v}' which is NOT in any card data-svc!")
        else:
            print(f"  ✅ MATCH: '{k}' => '{v}'")
else:
    print("Map not found in onboard.html!")
