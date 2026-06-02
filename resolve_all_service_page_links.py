import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

service_pages = [
    "gst-audit-compliance",
    "dpdp-readiness-assessment",
    "financial-operations-audit",
    "it-cybersecurity-audit",
    "export-compliance",
    "vextintel-monthly-retainer",
    "fema-compliance-audit",
    "soc2-readiness-assessment",
    "gdpr-compliance-assessment",
    "hipaa-compliance-assessment",
    "pci-dss-compliance-assessment",
    "iso27001-gap-assessment",
    "esg-baseline-report",
    "vendor-risk-assessment",
    "aml-kyc-policy-audit",
    "annual-compliance-subscription",
    "income-tax-compliance-audit",
    "msme-compliance-health-check",
    "payroll-compliance-audit",
    "startup-dpiit-compliance-audit",
    "transfer-pricing-documentation",
    "vextintel-global",
    "ai-business-process-intelligence",
    "ai-competitive-intelligence",
    "ai-market-entry-analysis",
    "ai-operational-risk-assessment"
]

print("Resolving all service pages root-relative links to local file links...")

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for page in service_pages:
        # Match href="/page" and replace with href="page.html"
        pattern = r'href="/' + page + r'"'
        repl = r'href="' + page + r'.html"'
        content_new, count = re.subn(pattern, repl, content)
        if count > 0:
            content = content_new
            modified = True
            
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  - Resolved links in: {file_name}")

print("\nDone resolving service links.")
