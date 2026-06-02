import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

results = []
for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    lines = content.split('\n')
    for idx, line in enumerate(lines):
        line_lower = line.lower()
        if "international" in line_lower:
            results.append(f"{file_name}:{idx+1}: {line.strip()}")

output_path = os.path.join(dir_path, "scratch", "international_matches.txt")
with open(output_path, 'w', encoding='utf-8') as out:
    out.write("\n".join(results))

print(f"Total matches found: {len(results)}. Written to {output_path}")
