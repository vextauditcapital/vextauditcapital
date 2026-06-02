import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
target_files = [
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

for f_name in target_files:
    f_path = os.path.join(dir_path, f_name)
    if not os.path.exists(f_path):
        print(f"File NOT found: {f_name}")
        continue
    with open(f_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Let's find all links (href) inside this file
    # We want to see where they go
    links = re.findall(r'href="([^"]+)"', content)
    # Filter links that are either rzp or onboard
    matched_links = [l for l in links if "rzp" in l or "onboard" in l]
    print(f"File: '{f_name}'")
    print(f"  Total matched links: {matched_links}")
    print("-" * 50)
