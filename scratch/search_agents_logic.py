import os
import re

agents_dir = r"C:\Users\shyam\.gemini\antigravity\scratch\agents"
py_files = []

for root, dirs, files in os.walk(agents_dir):
    for file in files:
        if file.endswith('.py'):
            py_files.append(os.path.join(root, file))

print(f"Scanning {len(py_files)} python files in agents...")

for file_path in sorted(py_files):
    rel_path = os.path.relpath(file_path, agents_dir)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    matches = []
    for line_num, line in enumerate(content.splitlines(), 1):
        line_lower = line.lower()
        if any(kw in line_lower for kw in ["welcome", "invoice", "receipt", "sow", "payment", "zoho", "sign"]):
            matches.append(f"  Line {line_num}: {line.strip()[:100]}")
            
    if matches:
        print(f"=== File: {rel_path} ===")
        for match in matches[:30]:  # Show first 30 matches
            print(match)
        if len(matches) > 30:
            print(f"  ... and {len(matches)-30} more matches")
        print()
