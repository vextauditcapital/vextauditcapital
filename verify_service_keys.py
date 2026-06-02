import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

# The map keys from onboard.html:
map_keys = {
    'process', 'competitive', 'market-entry', 'operational-risk',
    'gst', 'dpdp', 'financial', 'it', 'export', 'bundle', 'vextintel',
    'vextintel-annual', 'tds', 'roc', 'payroll', 'fema', 'msme', 'startup',
    'annual-subscription', 'amlkyc', 'esg', 'gdpr', 'hipaa', 'iso27001',
    'pcidss', 'soc2', 'transferpricing', 'vendor', 'vextintel-global', 'incometax'
}

print("Checking ?service= parameters in all HTML files against onboard.html map keys...\n")

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = re.findall(r'service=([\w-]+)', content)
    for m in matches:
        if m not in map_keys:
            print(f"WARNING: Key '{m}' in {file_name} is NOT in onboard.html's map!")
        else:
            # print(f"OK: '{m}' in {file_name}")
            pass
print("Done cross-verifying service keys.")
