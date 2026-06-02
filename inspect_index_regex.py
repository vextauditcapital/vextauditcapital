import re

file_path = r"C:\Users\shyam\.gemini\antigravity\scratch\index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all <a ... href="..." ...> ... </a> tags
a_tags = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.DOTALL | re.IGNORECASE)

print(f"Total links found in index.html: {len(a_tags)}")
for i, (href, text) in enumerate(a_tags):
    text_clean = re.sub(r'<[^>]+>', '', text).strip().replace('\n', ' ')
    if 'onboard' in href or 'rzp' in href:
        print(f"{i:3d}: text=\"{text_clean[:50]}\", href=\"{href}\"")
