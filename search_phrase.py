import os

phrases = ["USD pricing", "USD pricing available", "international clients", "Custom bundles", "Custom bundles on request", "on request"]
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print("Searching for disallowed phrases in HTML files...")
for fname in html_files:
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    for phrase in phrases:
        if phrase in content:
            print(f"File: {fname} | Found phrase: '{phrase}'")
            # find the line(s) containing it
            lines = content.split('\n')
            for idx, line in enumerate(lines, 1):
                if phrase in line:
                    print(f"  Line {idx:3d}: {line.strip()[:150]}")
