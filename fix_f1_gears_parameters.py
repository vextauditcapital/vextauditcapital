import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"

replacements = {
    "ai-operational-risk-assessment.html": [
        ("?service=operational-risk", "?service=ops-risk")
    ],
    "aml-kyc-policy-audit.html": [
        ("?service=amlkyc", "?service=aml-kyc")
    ],
    "annual-compliance-subscription.html": [
        ("?service=annual-subscription", "?service=annual-sub")
    ],
    "financial-operations-audit.html": [
        ("?service=financial", "?service=fin-ops")
    ],
    "income-tax-compliance-audit.html": [
        ("?service=incometax", "?service=income-tax")
    ],
    "it-cybersecurity-audit.html": [
        ("?service=it", "?service=it-cyber")
    ],
    "startup-dpiit-compliance-audit.html": [
        ("?service=startup", "?service=startup-dpiit")
    ],
    "transfer-pricing-documentation.html": [
        ("?service=transferpricing", "?service=transfer-pricing")
    ],
    "vendor-risk-assessment.html": [
        ("?service=vendor", "?service=vendor-risk")
    ],
    "vextintel-monthly-retainer.html": [
        ("?service=vextintel", "?service=vextintel-monthly")
    ]
}

print("Running Gears Routing Param Correcter...")
for filename, repl_list in replacements.items():
    file_path = os.path.join(dir_path, filename)
    if not os.path.exists(file_path):
        print(f"File not found: {filename}")
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    original_content = content
    for old, new in repl_list:
        content = content.replace(old, new)
        
    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filename}")
    else:
        print(f"No changes needed for {filename}")

print("Done!")
