with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's search for category buttons or filters
import re
print("Category buttons/tabs found:")
categories = re.findall(r'<button[^>]*class="[^"]*category-btn[^"]*"[^>]*>(.*?)</button>', text)
for cat in categories:
    print(f"  Category button: {cat.strip()}")

# Let's also see what categories the service cards have.
# Example: <div class="service-card ..." data-category="...">
cards_with_data_cat = re.findall(r'<div class="service-card[^"]*"[^>]*data-category="([^"]+)"', text)
print(f"Cards with data-category: {len(cards_with_data_cat)}")

# Let's search for all data-category values and their counts
from collections import Counter
print("Data categories found:", Counter(cards_with_data_cat))

# Let's see if there is JS that handles filtering
js_scripts = re.findall(r'<script>(.*?)</script>', text, re.DOTALL)
print(f"Number of inline script tags: {len(js_scripts)}")
for idx, script in enumerate(js_scripts):
    if "category" in script or "filter" in script or "active" in script:
        print(f"Script {idx+1} contains matching words. Length: {len(script)} chars")
        # Print first 20 lines of this script
        script_lines = script.strip().splitlines()
        print("\n".join(script_lines[:40]))
        print("...")
