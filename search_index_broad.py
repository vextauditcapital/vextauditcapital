import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search case insensitively
terms = ["usd", "pricing", "international", "custom", "bundle", "request", "dollar", r"\$"]
print("Broad searching index.html...")
for term in terms:
    matches = list(re.finditer(term, content, re.IGNORECASE))
    print(f"Term '{term}': Found {len(matches)} matches")
    for match in matches[:5]:
        start = max(0, match.start() - 60)
        end = min(len(content), match.end() + 60)
        print(f"  Match at index {match.start()}: ...{content[start:end].replace('\n', ' ')}...")
