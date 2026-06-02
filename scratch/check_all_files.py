import re

files_to_check = [
    "annual-compliance-subscription.html",
    "fema-compliance-audit.html",
    "gdpr-compliance-assessment.html",
    "payroll-compliance-audit.html",
    "startup-dpiit-compliance-audit.html"
]

print("==== INSPECTING DETAILED PAGES LINKS ====")
for f in files_to_check:
    fc = open(f, encoding="utf-8").read()
    links = re.findall(r'href=["\']([^"\']*)["\']', fc)
    ctas = [l for l in links if "onboard" in l or "rzp" in l or "PENDING" in l]
    print(f"\n{f}:")
    for c in set(ctas):
        print(f"  - {c}")
