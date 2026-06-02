import re
import sys

# Ensure UTF-8 output for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's search for id="pricing" and print that block of HTML
pricing_m = re.search(r'<section[^>]*id="pricing"[^>]*>(.*?)</section>', text, re.DOTALL)
if pricing_m:
    print("Pricing Section Found!")
    pricing_content = pricing_m.group(1)
    # Find all links (hrefs) in pricing section
    links = re.findall(r'href="([^"]+)"', pricing_content)
    print("Links in pricing section:", links)
    print("\nContent snippet of pricing section:")
    for line in pricing_content.strip().splitlines()[:40]:
        # Escape or replace unicode to prevent encoding crash
        print(" ", line.replace('\u20b9', 'Rs.'))
else:
    print("No pricing section found!")
