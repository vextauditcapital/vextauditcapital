import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all a tags containing onboard in href
matches = re.finditer(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.IGNORECASE | re.DOTALL)

print("Listing all onboarding links in index.html:")
print("=" * 60)
for idx, match in enumerate(matches, 1):
    href = match.group(1)
    text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
    text = re.sub(r'\s+', ' ', text)
    print(f"{idx:02d}. Href: '{href}' | Text: '{text[:50]}'")
print("=" * 60)
