import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

report = ["Audit of Razorpay Links in all HTML files:"]

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find any href containing rzp.io or razorpay
    hrefs = re.findall(r'href=["\']([^"\']*(?:rzp\.io|razorpay)[^"\']*)["\']', content, re.IGNORECASE)
    if hrefs:
        report.append(f"=== File: {file_name} ===")
        for href in hrefs:
            report.append(f"  - Direct Link: {href}")
        report.append("")

with open(r"C:\Users\shyam\.gemini\antigravity\scratch\scratch\rzp_links_found.txt", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(report))

print("Audit complete. Written to scratch/rzp_links_found.txt.")
