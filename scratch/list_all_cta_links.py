import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

report_lines = [f"Scanning CTAs in {len(html_files)} HTML files...\n"]

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all <a href="...">text</a> tags
    links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.IGNORECASE | re.DOTALL)
    
    # Filter CTAs
    ctas = []
    for href, text in links:
        # Clean text
        text_clean = re.sub(r'<[^>]+>', '', text).strip()
        text_clean = re.sub(r'\s+', ' ', text_clean)
        
        # Check if it's a potential CTA or onboarding link
        if 'onboard' in href or 'rzp' in href or 'checkout' in href or 'payment' in href or 'pay' in href or 'buy' in href or 'get' in href or 'start' in href:
            ctas.append(f"a[href='{href}'] (text: '{text_clean}')")
            
    # Also find buttons with onclick
    buttons = re.findall(r'<button\s+[^>]*onclick=["\']([^"\']+)["\'][^>]*>(.*?)</button>', content, re.IGNORECASE | re.DOTALL)
    for onclick, text in buttons:
        text_clean = re.sub(r'<[^>]+>', '', text).strip()
        text_clean = re.sub(r'\s+', ' ', text_clean)
        ctas.append(f"button[onclick='{onclick}'] (text: '{text_clean}')")

    if ctas:
        report_lines.append(f"=== {file_name} ===")
        for cta in ctas:
            report_lines.append(f"  - {cta}")
        report_lines.append("")

with open(r"C:\Users\shyam\.gemini\antigravity\scratch\scratch\cta_links_report.txt", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(report_lines))

print("Scan complete. Written to scratch/cta_links_report.txt.")
