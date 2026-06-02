import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

scripts = re.findall(r'<script>(.*?)</script>', text, re.DOTALL)
print(f"Total script tags: {len(scripts)}")
for idx, script in enumerate(scripts):
    print(f"Script {idx+1}:")
    print(script.strip())
    print("=" * 60)
