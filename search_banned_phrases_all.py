import os
import re
import sys

# Ensure UTF-8 printing
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

phrases = [
    r"USD pricing available for international clients",
    r"Custom bundles on request",
    r"USD pricing",
    r"Custom bundles"
]

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print("Searching case-insensitively for disallowed phrases in all HTML files...")
for fname in html_files:
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    for phrase in phrases:
        pattern = re.compile(phrase, re.IGNORECASE)
        matches = list(pattern.finditer(content))
        if matches:
            print(f"\nFile: {fname} | Match for '{phrase}':")
            for m in matches:
                # Get the surrounding line or text
                start = max(0, m.start() - 100)
                end = min(len(content), m.end() + 100)
                snippet = content[start:end].replace('\n', ' ')
                print(f"  Pos {m.start()}: ...{snippet}...")
