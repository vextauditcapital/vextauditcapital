import re

content = open("index.html", encoding="utf-8").read()
lines = content.splitlines()

print("==== DIRECT RAZORPAY LINKS IN INDEX.HTML ====")
for idx, line in enumerate(lines):
    matches = re.findall(r'href=["\'](https?://rzp\.io/[^\s"\']+)["\']', line)
    if matches:
        print(f"Line {idx+1}: {line.strip()}")
