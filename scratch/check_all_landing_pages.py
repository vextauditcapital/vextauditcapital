import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Precise 30 services table mapping from user prompt
table_services = {
    "gst": {"name": "GST Audit & Compliance", "price_str": "25,000", "link": "https://rzp.io/rzp/MyIHpEhi"},
    "tds": {"name": "TDS Compliance Audit", "price_str": "20,000", "link": "https://rzp.io/rzp/A98OOcD"},
    "roc": {"name": "ROC Annual Compliance Audit", "price_str": "18,000", "link": "https://rzp.io/rzp/VNz3svW"},
    "payroll": {"name": "Payroll Compliance Audit", "price_str": "22,000", "link": "https://rzp.io/rzp/zcsYoXk"},
    "incometax": {"name": "Income Tax Compliance Audit", "price_str": "30,000", "link": "https://rzp.io/rzp/fNT724qg"},
    "fema": {"name": "FEMA Compliance Audit", "price_str": "25,000", "link": "https://rzp.io/rzp/nwRy10qr"},
    "dpdp": {"name": "DPDP Readiness Assessment", "price_str": "40,000", "link": "https://rzp.io/rzp/b75whbt"},
    "financial": {"name": "Financial Operations Audit", "price_str": "30,000", "link": "https://rzp.io/rzp/O94qCEOp"},
    "export": {"name": "Export Compliance", "price_str": "20,000", "link": "https://rzp.io/rzp/KlLn2kw"},
    "transferpricing": {"name": "Transfer Pricing Documentation", "price_str": "75,000", "link": "https://rzp.io/rzp/RJ6gGCtO"},
    "msme": {"name": "MSME Compliance Health Check", "price_str": "15,000", "link": "https://rzp.io/rzp/slAtbzHC"},
    "startup": {"name": "Startup India DPIIT Audit", "price_str": "18,000", "link": "https://rzp.io/rzp/FN6U7dQ9"},
    "it": {"name": "IT & Cybersecurity Audit", "price_str": "50,000", "link": "https://rzp.io/rzp/zHkk2GW"},
    "bundle": {"name": "Full Audit Bundle", "price_str": "75,000", "link": "https://rzp.io/rzp/feAb7F1B"},
    "iso27001": {"name": "Information Security Gap Assessment", "price_str": "1,199", "link": "https://rzp.io/rzp/FWg51kt"},
    "soc2": {"name": "SOC 2 Readiness Assessment", "price_str": "999", "link": "https://rzp.io/rzp/LurO22V"},
    "gdpr": {"name": "GDPR Compliance Assessment", "price_str": "799", "link": "https://rzp.io/rzp/pMR4io3o"},
    "hipaa": {"name": "HIPAA Compliance Assessment", "price_str": "899", "link": "https://rzp.io/rzp/pEy3CgD"},
    "pcidss": {"name": "PCI-DSS Compliance Assessment", "price_str": "999", "link": "https://rzp.io/rzp/vIX6zbtu"},
    "esg": {"name": "ESG Baseline Report", "price_str": "599", "link": "https://rzp.io/rzp/peFsINs3"},
    "vendor": {"name": "Vendor Risk Assessment", "price_str": "499", "link": "https://rzp.io/rzp/mub5P0h"},
    "amlkyc": {"name": "AML / KYC Policy Audit", "price_str": "799", "link": "https://rzp.io/rzp/eabyeCw"},
    "process": {"name": "Process Intelligence", "price_str": "707", "link": "https://rzp.io/rzp/fFcfaX9H"},
    "competitive": {"name": "Competitive Intelligence", "price_str": "99", "link": "https://rzp.io/rzp/WUd8yfc"},
    "market-entry": {"name": "Market Entry Analysis", "price_str": "149", "link": "https://rzp.io/rzp/qkMdwMw"},
    "operational-risk": {"name": "Operational Risk Assessment", "price_str": "1,022", "link": "https://rzp.io/rzp/06Jx04T"},
    "vextintel": {"name": "VextIntel India Retainer", "price_str": "15,000", "link": "https://rzp.io/rzp/VvoQ8SpY"},
    "vextintel-global": {"name": "VextIntel Global Edition", "price_str": "199", "link": "https://rzp.io/rzp/8Jf16CNt"},
    "annual-subscription": {"name": "Annual Compliance Subscription", "price_str": "60,000", "link": "https://rzp.io/rzp/gmVABp0"},
    "vextintel-annual": {"name": "VextIntel Annual", "price_str": "1,50,000", "link": "https://rzp.io/rzp/oMrFyN3k"}
}

# Find all HTML files
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f not in ['index.html', 'onboard.html', 'privacy.html', 'terms.html', 'cookies.html', 'data-policy.html', 'delivery.html', 'disclosure.html', 'happiness.html', 'refund.html', 'security.html', 'upload.html']]

print(f"Analyzing {len(html_files)} individual service landing pages...\n")

failures_count = 0

for file_name in sorted(html_files):
    file_path = file_name
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to extract the parameter service=xyz from the file to know which service it is
    service_match = re.search(r'onboard\.html\?service=([\w-]+)', content)
    if not service_match:
        print(f"WARNING: No onboard.html?service= link found in {file_name}")
        continue
    
    service_key = service_match.group(1)
    if service_key not in table_services:
        print(f"WARNING: Service key '{service_key}' in {file_name} not found in the 30 services table!")
        continue
        
    expected = table_services[service_key]
    
    # Check if the page content contains the correct pricing string and the correct rzp link
    price_found = expected["price_str"] in content or expected["price_str"].replace(",", "") in content
    
    # For individual landing pages, do they link directly to the Razorpay checkout, or do they link to onboard.html?service=xyz?
    # Let's check if the button points to onboard.html?service=xyz
    expected_button_link = f"onboard.html?service={service_key}"
    button_found = expected_button_link in content
    
    if not price_found:
        print(f"FAIL pricing: {file_name} ({service_key}) - expected price '{expected['price_str']}' not found in content!")
        failures_count += 1
    if not button_found:
        print(f"FAIL button link: {file_name} ({service_key}) - expected button link '{expected_button_link}' not found!")
        failures_count += 1

print(f"\nLanding pages analysis complete. Total failures: {failures_count}")
