import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
specific_files = [
    'gst-audit-compliance.html',
    'dpdp-readiness-assessment.html',
    'financial-operations-audit.html',
    'it-cybersecurity-audit.html',
    'export-compliance.html',
    'vextintel-monthly-retainer.html'
]

for file_name in specific_files:
    file_path = os.path.join(dir_path, file_name)
    if not os.path.exists(file_path):
        print(f"Not found: {file_name}")
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all hrefs
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
    onboard_hrefs = [h for h in hrefs if 'onboard' in h or 'rzp' in h]
    print(f"{file_name}: {onboard_hrefs}")
