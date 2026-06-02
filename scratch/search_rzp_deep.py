import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

print(f"Deep scanning {len(html_files)} HTML files for 'rzp' or 'razorpay'...")

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check for rzp or razorpay
    matches = []
    # Find surrounding context for any matches
    for line_num, line in enumerate(content.splitlines(), 1):
        if 'rzp' in line.lower() or 'razorpay' in line.lower():
            matches.append(f"  Line {line_num}: {line.strip()[:120]}")
            
    if matches:
        print(f"=== {file_name} ===")
        for match in matches:
            print(match)
        print()
