import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

print("Outbound links in all HTML files:")
for file_name in sorted(html_files):
    if file_name in ['onboard.html', 'index.html', 'privacy.html', 'terms.html', 'refund.html', 'security.html', 'data-policy.html', 'disclosure.html', 'cookies.html', 'delivery.html']:
        continue
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    hrefs = re.findall(r'href="([^"]+)"', content)
    print(f"=== {file_name} ===")
    for h in hrefs:
        print(f"  - {h}")
