import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"

patterns = [
    r"usd\s+pricing\s+available",
    r"custom\s+bundles\s+on\s+request",
    r"usd\s+pricing",
    r"custom\s+bundles"
]

results = []
for root, dirs, files in os.walk(dir_path):
    if ".git" in root:
        continue
    for file_name in files:
        if file_name.endswith('.html') or file_name.endswith('.js') or file_name.endswith('.css') or file_name.endswith('.md'):
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception:
                continue
            
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for m in matches:
                    start_char = max(0, m.start() - 50)
                    end_char = min(len(content), m.end() + 50)
                    snippet = content[start_char:end_char].replace('\n', ' ')
                    rel_path = os.path.relpath(file_path, dir_path)
                    results.append(f"{rel_path}: '{m.group()}' near: ...{snippet}...")

print(f"Total loose matches: {len(results)}")
for r in results:
    print(r)
