import os
import re

service_files = [
    "tds-compliance-audit.html",
    "fema-compliance-audit.html",
    "roc-annual-compliance-audit.html",
    "payroll-compliance-audit.html",
    "annual-compliance-subscription.html",
    "msme-compliance-health-check.html",
    "startup-dpiit-compliance-audit.html",
    "ai-business-process-intelligence.html",
    "ai-competitive-intelligence.html",
    "ai-market-entry-analysis.html",
    "ai-operational-risk-assessment.html"
]

print("Inspecting links in specific service pages...")
for fname in service_files:
    if not os.path.exists(fname):
        print(f"File not found: {fname}")
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    print(f"\n--- {fname} ---")
    # Find all hrefs
    hrefs = re.findall(r'href=["\']([^"\']*)["\']', content)
    for href in hrefs:
        if 'onboard' in href or 'rzp' in href or 'razorpay' in href or 'http' in href:
            print(f"  href: {href}")
            
    # Also find any inline scripts or onclick attributes
    onclicks = re.findall(r'onclick=["\']([^"\']*)["\']', content)
    for onclick in onclicks:
        print(f"  onclick: {onclick}")
