import os
import re

root_path = r"C:\Users\shyam\.gemini\antigravity\scratch"

found = False
for root, dirs, files in os.walk(root_path):
    # Skip standard git, cache, or environment directories
    if any(p in root for p in ['.git', '__pycache__', 'env', 'node_modules']):
        continue
    
    for file_name in files:
        if file_name.endswith('.html'):
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                continue
            
            # Find direct RZP links (ignoring onboard.html)
            if file_name != 'onboard.html':
                matches = re.findall(r'href=["\'](https?://rzp\.io/rzp/[^"\']+)["\']', content, re.IGNORECASE)
                if matches:
                    print(f"FOUND direct RZP link in {os.path.relpath(file_path, root_path)}:")
                    for m in matches:
                        print(f"  - {m}")
                    found = True

if not found:
    print("No HTML files in the entire project (recursively) contain direct Razorpay links outside of onboard.html.")
