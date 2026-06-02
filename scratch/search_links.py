import glob
import re

html_files = glob.glob("*.html")
print(f"Searching {len(html_files)} HTML files for direct rzp.io links:")

for f in html_files:
    content = open(f, encoding="utf-8").read()
    matches = re.findall(r'href=["\'](https?://rzp\.io/[^\s"\']+)["\']', content)
    if matches:
        print(f"\nFile: {f} ({len(matches)} direct links)")
        for m in matches:
            print(f"  - {m}")
