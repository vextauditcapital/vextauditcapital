import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"

results = []
for root, dirs, files in os.walk(dir_path):
    # skip .git
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
                if "usd pricing available" in line_lower or "custom bundles" in line_lower:
                    rel_path = os.path.relpath(file_path, dir_path)
                    results.append(f"{rel_path}:{idx+1}: {line.strip()}")

output_path = os.path.join(dir_path, "scratch", "recursive_disclaimer_matches.txt")
with open(output_path, 'w', encoding='utf-8') as out:
    out.write("\n".join(results))

print(f"Total matches found recursively: {len(results)}. Written to {output_path}")
for r in results:
    print(r)
