import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

print("Searching all HTML files for any Razorpay (rzp.io) links...")
found = False

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for direct razorpay links
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if "rzp.io" in line or "razorpay" in line.lower():
            print(f"[{file_name}:{i+1}]: {line.strip()}")
            found = True

if not found:
    print("NO raw Razorpay links found in any files outside onboard.html!")
