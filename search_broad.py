import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

results = []
for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # search for 'USD' or 'bundle' or 'custom'
    lines = content.split('\n')
    for idx, line in enumerate(lines):
        if 'usd' in line.lower() or 'bundle' in line.lower() or 'custom' in line.lower():
            results.append(f"{file_name}:{idx+1}: {line.strip()}")

output_path = os.path.join(dir_path, "detailed_usd_bundle_matches.txt")
with open(output_path, 'w', encoding='utf-8') as out:
    out.write("\n".join(results))

print(f"Done. Found {len(results)} matches. Saved to detailed_usd_bundle_matches.txt")
