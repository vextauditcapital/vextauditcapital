import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith(".html")]

print(f"Total HTML files: {len(html_files)}")
print("\nFiles containing rzp.io links:")

for f_name in html_files:
    f_path = os.path.join(dir_path, f_name)
    with open(f_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    links = re.findall(r'href="([^"]*rzp\.io[^"]*)"', content)
    if links:
        print(f"File: '{f_name}' has {len(links)} links:")
        for l in links:
            print("  -", l)
