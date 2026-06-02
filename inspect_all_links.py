import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

print(f"Scanning {len(html_files)} HTML files for hrefs containing 'onboard' or 'rzp'...")

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all hrefs
    hrefs = re.findall(r'href="([^"]+)"', content)
    # Filter for onboarding or razorpay or action links
    target_hrefs = [h for h in hrefs if "onboard" in h or "rzp" in h]
    
    if target_hrefs:
        print(f"\n=== {file_name} ===")
        for h in target_hrefs:
            print(f"  - {h}")
