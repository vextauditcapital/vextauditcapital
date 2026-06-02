import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

# List of files to skip
exclude = ['onboard.html', 'index.html', 'privacy.html', 'terms.html', 'refund.html', 'cookies.html', 'data-policy.html', 'disclosure.html', 'security.html', 'happiness.html', 'upload.html', 'delivery.html']

service_files = [f for f in html_files if f not in exclude]

print(f"Scanning scripts and onclick handlers in {len(service_files)} service files...")

for file_name in sorted(service_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    onclicks = re.findall(r'onclick=["\']([^"\']+)["\']', content, re.IGNORECASE)
    
    if scripts or onclicks:
        print(f"=== File: {file_name} ===")
        if scripts:
            print(f"  Found {len(scripts)} script block(s):")
            for idx, s in enumerate(scripts, 1):
                print(f"    Script {idx}: {s.strip()[:100]}...")
        if onclicks:
            print(f"  Found onclick handler(s): {set(onclicks)}")
        print()
