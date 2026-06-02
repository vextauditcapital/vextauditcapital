import re

with open('onboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

sc_divs = re.findall(r'<div class="sc"[^>]*>', content)
for idx, div in enumerate(sc_divs, 1):
    print(f"{idx}: {div}")
