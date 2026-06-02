import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # search for 'rzp' case-insensitive
    matches = re.findall(r'.{0,100}rzp.{0,100}', content, re.IGNORECASE)
    if matches and file_name != 'onboard.html':
        print(f"=== {file_name} has matches ===")
        for m in matches[:5]:
            print("  ", m.strip())
