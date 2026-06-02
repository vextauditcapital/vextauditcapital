import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for "USD", "dollar", "request", "bundle" (case-insensitive)
matches = []
for i, line in enumerate(content.splitlines()):
    if any(term in line.lower() for term in ["usd", "dollar", "request", "bundle"]):
        matches.append(f"{i+1}: {line.strip()}")

print(f"Found {len(matches)} potential matches in index.html:")
for m in matches:
    print(m)
