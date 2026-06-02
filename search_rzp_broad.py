import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith(".html")]

print(f"Total HTML files: {len(html_files)}")
print("\nFiles containing rzp.io occurrences:")

for f_name in html_files:
    f_path = os.path.join(dir_path, f_name)
    with open(f_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # search for raw rzp.io string
    matches = re.findall(r'rzp\.io/rzp/[a-zA-Z0-9_-]+', content)
    if matches:
        print(f"File: '{f_name}' has {len(matches)} occurrences of rzp.io:")
        for m in set(matches):
            print("  -", m)
