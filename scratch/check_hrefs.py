import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
for f_name in os.listdir(dir_path):
    if f_name.endswith('.html'):
        path = os.path.join(dir_path, f_name)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Find all hrefs
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
        onboard_hrefs = [h for h in hrefs if 'onboard' in h or 'rzp' in h]
        if onboard_hrefs:
            print(f"{f_name}:")
            for h in onboard_hrefs:
                print(f"  - {h}")
