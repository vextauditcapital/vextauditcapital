import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith(".html") and f not in ["index.html", "onboard.html", "upload.html", "privacy.html", "cookies.html", "terms.html", "data-policy.html", "disclosure.html", "happiness.html", "delivery.html", "refund.html", "security.html"]]

print(f"Total service pages: {len(html_files)}")

for f_name in html_files:
    f_path = os.path.join(dir_path, f_name)
    with open(f_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find all links (hrefs) in this page
    # Look for any links containing rzp.io or onboard.html or other interesting targets
    rzp_links = re.findall(r'href="([^"]*rzp\.io[^"]*)"', content)
    onboard_links = re.findall(r'href="([^"]*onboard\.html[^"]*)"', content)
    
    # Let's find the main CTA button or link
    # For example, look for class="cta-button" or "btn" or similar class in <a href="...">
    ctas = re.findall(r'<a[^>]*class="[^"]*cta-[^"]*"[^>]*href="([^"]+)"', content)
    if not ctas:
        # Fallback to any button/link that says "Get Started" or "Buy" or "Initiate" or "Book"
        ctas = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>([^<]*(?:Get Started|Buy|Pay|Book|Initiate|Onboard|Subscribe|Purchase|Start)[^<]*)</a>', content, re.I)
        
    print(f"File: '{f_name}'")
    print(f"  Razorpay links: {rzp_links}")
    print(f"  Onboard links: {onboard_links}")
    print(f"  CTAs found: {ctas}")
    print("-" * 50)
