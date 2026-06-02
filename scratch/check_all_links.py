import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

print(f"Scanning links in {len(html_files)} HTML files...\n")

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all href links
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
    onboard_with_service = []
    onboard_without_service = []
    direct_rzp = []
    other_htmls = []
    
    for href in hrefs:
        if 'onboard.html' in href or 'onboard?' in href or href == 'onboard':
            if 'service=' in href:
                onboard_with_service.append(href)
            else:
                onboard_without_service.append(href)
        elif 'rzp.io' in href or 'razorpay' in href:
            direct_rzp.append(href)
        elif href.endswith('.html') and href != 'onboard.html':
            other_htmls.append(href)
            
    if onboard_without_service or direct_rzp:
        print(f"=== {file_name} ===")
        if onboard_with_service:
            print(f"  Valid Onboard links with service: {set(onboard_with_service)}")
        if onboard_without_service:
            print(f"  WARNING: Onboard links WITHOUT service query: {set(onboard_without_service)}")
        if direct_rzp:
            print(f"  WARNING: DIRECT Razorpay links: {set(direct_rzp)}")
        print()
