import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

words = [r"\busd\b", r"\$", r"request", r"international", r"bundle"]

print("Searching for any occurrences of the terms in all HTML files...")
for fname in html_files:
    # Skip terms, privacy, security, refund, cookies, delivery, data-policy, disclosure, upload
    if fname in ['privacy.html', 'terms.html', 'security.html', 'refund.html', 'cookies.html', 'delivery.html', 'data-policy.html', 'disclosure.html', 'upload.html']:
        continue
        
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    found_any = False
    for word in words:
        matches = list(re.finditer(word, content, re.IGNORECASE))
        if matches:
            if not found_any:
                print(f"\n================ FILE: {fname} ================")
                found_any = True
            print(f"  Word: '{word}' -> Found {len(matches)} matches")
            for m in matches[:3]:  # Print first 3 matches
                start = max(0, m.start() - 60)
                end = min(len(content), m.end() + 60)
                snippet = content[start:end].replace('\n', ' ').strip()
                print(f"    Line around pos {m.start()}: ...{snippet}...")
