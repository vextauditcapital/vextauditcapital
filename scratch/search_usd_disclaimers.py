import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

targets = ["usd pricing available", "custom bundles on request", "custom bundles"]

results = []
for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    lines = content.split('\n')
    for idx, line in enumerate(lines):
        line_lower = line.lower()
        for target in targets:
            if target in line_lower:
                results.append(f"{file_name}:{idx+1} [{target}]: {line.strip()}")

for r in results:
    print(r)

print(f"Total matches found: {len(results)}")
