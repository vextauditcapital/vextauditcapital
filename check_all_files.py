import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

output_lines = []
output_lines.append(f"Auditing {len(html_files)} HTML files for pricing and Razorpay links...\n")

for file_name in html_files:
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    rzp_links = re.findall(r'rzp\.io/rzp/\w+', content)
    prices_rs = re.findall(r'(?:Rs\.|₹|INR)\s*[\d,]+', content)
    prices_usd = re.findall(r'\$\s*[\d,]+', content)
    
    if rzp_links or prices_rs or prices_usd:
        output_lines.append(f"File: {file_name}")
        if rzp_links:
            output_lines.append(f"  Razorpay links: {list(set(rzp_links))}")
        if prices_rs:
            output_lines.append(f"  Rupee prices: {list(set(prices_rs))[:6]}")
        if prices_usd:
            output_lines.append(f"  USD prices: {list(set(prices_usd))[:6]}")
        output_lines.append("-" * 50)

with open('audit_results.txt', 'w', encoding='utf-8') as f_out:
    f_out.write("\n".join(output_lines))

print("Audit completed successfully. Results written to audit_results.txt.")
