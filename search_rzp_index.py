with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
rzp_links = re.findall(r'href="([^"]*rzp\.io[^"]*)"', text)
print(f"Razorpay links in index.html: {len(rzp_links)}")
for l in rzp_links:
    print(" ", l)
