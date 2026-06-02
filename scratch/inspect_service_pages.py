import os
import re

dir_path = '.'
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

output = []

for file_name in html_files:
    if file_name in ['index.html', 'onboard.html', 'upload.html']:
        continue
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's find all hrefs in this file
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
    # Let's find all button clicks or links or forms
    rzp_links = re.findall(r'rzp\.io/rzp/\w+', content)
    prices = re.findall(r'(?:₹|Rs\.|USD|\$)\s*[0-9,]+', content)
    
    output.append(f"=== {file_name} ===")
    output.append(f"  Hrefs: {hrefs}")
    output.append(f"  Razorpay links: {rzp_links}")
    output.append(f"  Prices: {list(set(prices))}")
    output.append("")

with open('detailed_service_inspect.txt', 'w', encoding='utf-8') as f_out:
    f_out.write('\n'.join(output))

print("Inspection complete.")
