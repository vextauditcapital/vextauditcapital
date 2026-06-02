import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'<div class="service-card[^>]*>.*?iso27001-gap-assessment\.html.*?</a>\s*</div>', '', content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("ISO removed.")