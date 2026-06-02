import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's search for any script block or event handlers
scripts = re.findall(r'<script>(.*?)</script>', text, re.DOTALL)
print(f"Number of scripts: {len(scripts)}")
for idx, script in enumerate(scripts):
    print(f"Script {idx+1}:")
    print(script)
    print("-" * 50)
    
# Let's search for any onclick attributes on HTML tags
onclicks = re.findall(r'onclick="([^"]+)"', text)
print(f"Onclicks found: {onclicks}")

# Let's search for any data-link or data-payment or razorpay inside index.html
matches = re.findall(r'data-[a-zA-Z0-9_-]+="[^"]+"', text)
print(f"Data attributes found: {len(matches)}")
for m in matches[:10]:
    print(" ", m)
