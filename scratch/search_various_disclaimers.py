import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"

targets = [
    "usd pricing",
    "international clients",
    "custom bundles",
    "on request",
    "available for international clients"
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
            
            lines = content.split('\n')
            for idx, line in enumerate(lines):
                line_lower = line.lower()
                for target in targets:
                    if target in line_lower:
                        rel_path = os.path.relpath(file_path, dir_path)
                        results.append(f"{rel_path}:{idx+1} [{target}]: {line.strip()}")

output_path = os.path.join(dir_path, "scratch", "various_disclaimer_matches.txt")
with open(output_path, 'w', encoding='utf-8') as out:
    out.write("\n".join(results))

print(f"Total matches found recursively: {len(results)}. Written to {output_path}")
for r in results[:30]: # print up to 30 matches
    try:
        print(r)
    except Exception:
        pass
