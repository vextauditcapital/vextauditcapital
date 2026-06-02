import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print("Searching for rzp.io in all HTML files:")
for f_path in html_files:
    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    matches = re.findall(r'rzp\.io/rzp/\w+', content)
    if matches:
        print(f"\nFile: {f_path}")
        print(f"  Matches: {list(set(matches))}")
