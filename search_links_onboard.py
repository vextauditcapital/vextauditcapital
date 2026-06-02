import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print("Searching for razorpay links in HTML files...")
for fname in html_files:
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # find rzp.io or razorpay
    matches = re.findall(r'href=["\'](https?://[^"\']*(?:rzp\.io|razorpay)[^"\']*)["\']', content)
    if matches:
        print(f"\nFile: {fname}")
        for match in matches:
            print(f"  Found Razorpay link: {match}")
