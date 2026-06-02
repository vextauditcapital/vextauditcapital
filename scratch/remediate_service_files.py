import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"

# Service file mapping
file_to_service = {
    'aml-kyc-policy-audit.html': 'amlkyc',
    'annual-compliance-subscription.html': 'annual-subscription',
    'esg-baseline-report.html': 'esg',
    'fema-compliance-audit.html': 'fema',
    'gdpr-compliance-assessment.html': 'gdpr',
    'hipaa-compliance-assessment.html': 'hipaa',
    'income-tax-compliance-audit.html': 'incometax',
    'iso27001-gap-assessment.html': 'iso27001',
    'msme-compliance-health-check.html': 'msme',
    'payroll-compliance-audit.html': 'payroll',
    'pci-dss-compliance-assessment.html': 'pcidss',
    'soc2-readiness-assessment.html': 'soc2',
    'startup-dpiit-compliance-audit.html': 'startup',
    'transfer-pricing-documentation.html': 'transferpricing',
    'vendor-risk-assessment.html': 'vendor',
    'vextintel-global.html': 'vextintel-global'
}

print("Remediating specific service detail HTML files to enforce service parameters...\n")

for file_name, service_key in file_to_service.items():
    file_path = os.path.join(dir_path, file_name)
    if not os.path.exists(file_path):
        print(f"File not found: {file_name}")
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace href="/onboard" or href='/onboard' or href="/onboard/" or href='/onboard/'
    # but NOT if it already has a query parameter like ?service=
    pattern = r'href\s*=\s*["\']/onboard/?["\']'
    replacement = f'href="/onboard?service={service_key}"'
    
    modified_content, count = re.subn(pattern, replacement, content)
    
    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"Updated {file_name}: replaced {count} generic '/onboard' links with parameterized ones.")
    else:
        print(f"No generic '/onboard' links found in {file_name}.")
        
print("\nRemediation complete!")
