import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('onboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Match pattern for <div class="sc" ...>
# Pattern: <div class="sc" data-svc="([^"]+)" data-amt="([^"]+)" data-lnk="([^"]+)">
# Followed by <div class="sc-n">([^<]+)</div><div class="sc-p">([^<]+)</div></div>
sc_pattern = re.compile(
    r'<div class="sc"\s+data-svc="([^"]+)"\s+data-amt="([^"]+)"\s+data-lnk="([^"]+)">\s*'
    r'<div class="sc-n">([^<]+)</div>\s*<div class="sc-p">([^<]+)</div>'
)

matches = sc_pattern.findall(content)

print(f"Found {len(matches)} services in HTML body:")
for i, m in enumerate(matches):
    print(f"{i+1}: svc='{m[0]}' | amt='{m[1]}' | lnk='{m[2]}' | name='{m[3]}' | price='{m[4]}'")
