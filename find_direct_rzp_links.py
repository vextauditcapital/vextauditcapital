import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

found = False
for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    hrefs = re.findall(r'href="([^"]+)"', content)
    for h in hrefs:
        if 'rzp' in h or 'razorpay' in h.lower():
            if file_name != 'onboard.html':
                print(f"FOUND direct RZP link in {file_name}: href=\"{h}\"")
                found = True

if not found:
    print("NO DIRECT RAZORPAY LINKS FOUND IN ANY HTML FILES OTHER THAN onboard.html")
