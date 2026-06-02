import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find all href links
hrefs = re.findall(r'href="([^"]+)"', content)
print("All hrefs in index.html:")
for h in sorted(set(hrefs)):
    if "onboard" in h or "rzp" in h or ".html" in h:
        print(f"  - {h}")
