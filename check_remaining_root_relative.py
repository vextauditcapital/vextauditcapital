import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

print("Checking for remaining root-relative links (href=\"/...\" or src=\"/...\")...")
found = False

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Exclude external absolute URLs starting with http or double slash, but catch root-relative
    href_matches = re.findall(r'href="(/[^/#"][^"]*)"', content)
    src_matches = re.findall(r'src="(/[^"][^"]*)"', content)
    
    if href_matches or src_matches:
        print(f"=== {file_name} ===")
        for m in href_matches:
            print(f"  Remaining root-relative href: {m}")
            found = True
        for m in src_matches:
            print(f"  Remaining root-relative src: {m}")
            found = True

if not found:
    print("NO REMAINING ROOT-RELATIVE LINKS FOUND! ALL LINKS ARE RELATIVE! 🎉")
