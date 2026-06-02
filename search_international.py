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
        if 'international' in line.lower() or 'pricing' in line.lower() or 'custom' in line.lower() or 'bundle' in line.lower():
            results.append(f"{file_name}:{idx+1}: {line.strip()}")

output_path = os.path.join(dir_path, "search_international_output.txt")
with open(output_path, 'w', encoding='utf-8') as out:
    out.write("\n".join(results))

print(f"Done. Saved to search_international_output.txt")
