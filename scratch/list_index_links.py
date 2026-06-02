import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

links = set(re.findall(r'href="([^"]+\.html[^"]*)"', content))
print("--- Links found in index.html ---")
for l in sorted(links):
    print(l)
