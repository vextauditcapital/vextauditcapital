import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

# Correct verified dashboard parameters from user's live setup
CORRECT_LINKS = {
    "GST Audit & Compliance": {
        "price": "INR 25,000",
        "link": "https://rzp.io/rzp/c8Iadz3e"
    },
    "DPDP Readiness Assessment": {
        "price": "INR 40,000",
        "link": "https://rzp.io/rzp/kbkHHpJU"
    },
    "Financial Operations Audit": {
        "price": "INR 30,000",
        "link": "https://rzp.io/rzp/jInJsXH9"
    },
    "IT & Cybersecurity Audit": {
        "price": "INR 50,000",
        "link": "https://rzp.io/rzp/tffBCbc3m"
    },
    "Export Compliance Audit": {
        "price": "INR 20,000",
        "link": "https://rzp.io/rzp/d6lMSsm"
    },
    "Export Compliance": {
        "price": "INR 20,000",
        "link": "https://rzp.io/rzp/d6lMSsm"
    },
    "VextIntel Monthly Retainer": {
        "price": "INR 15,000/month",
        "link": "https://rzp.io/rzp/xfTGpOLS"
    },
    "VextIntel India Retainer": {
        "price": "INR 15,000/month",
        "link": "https://rzp.io/rzp/xfTGpOLS"
    },
    "VextIntel Annual": {
        "price": "INR 1,50,000/year",
        "link": "https://rzp.io/rzp/f4Njslv"
    },
    "Full Audit Bundle": {
        "price": "INR 75,000",
        "link": "https://rzp.io/rzp/9AMfMA3"
    },
    "AI Business Process Intelligence": {
        "price": "$807",
        "link": "https://rzp.io/rzp/iY8ndF1"
    },
    "Process Intelligence": {
        "price": "$807",
        "link": "https://rzp.io/rzp/iY8ndF1"
    },
    "AI Competitive Intelligence": {
        "price": "$699",
        "link": "https://rzp.io/rzp/GwTyPEN"
    },
    "Competitive Intelligence": {
        "price": "$699",
        "link": "https://rzp.io/rzp/GwTyPEN"
    },
    "AI Market Entry Analysis": {
        "price": "$914",
        "link": "https://rzp.io/rzp/RfGnqkck"
    },
    "Market Entry Analysis": {
        "price": "$914",
        "link": "https://rzp.io/rzp/RfGnqkck"
    },
    "AI Operational Risk Assessment": {
        "price": "$1,022",
        "link": "https://rzp.io/rzp/TeVr6dJa"
    },
    "Operational Risk Assessment": {
        "price": "$1,022",
        "link": "https://rzp.io/rzp/TeVr6dJa"
    }
}

SECONDARY_SERVICES = {
    "TDS Compliance Audit": {
        "price": "INR 20,000",
        "link": "https://rzp.io/rzp/0sb2WvK"
    },
    "FEMA Compliance Audit": {
        "price": "INR 25,000",
        "link": "https://rzp.io/rzp/vDEsdOBV"
    },
    "ROC / MCA Annual Compliance": {
        "price": "INR 18,000",
        "link": "https://rzp.io/rzp/93UPUVP8"
    },
    "ROC Annual Compliance Audit": {
        "price": "INR 18,000",
        "link": "https://rzp.io/rzp/93UPUVP8"
    },
    "Payroll Compliance Audit": {
        "price": "INR 22,000",
        "link": "https://rzp.io/rzp/vkOc0Y4U"
    },
    "Annual Compliance Subscription": {
        "price": "INR 60,000",
        "link": "https://rzp.io/rzp/xvfP2ffr"
    },
    "MSME Compliance Health Check": {
        "price": "INR 15,000",
        "link": "https://rzp.io/rzp/X9O3urP"
    },
    "Startup DPIIT Compliance Audit": {
        "price": "INR 18,000",
        "link": "https://rzp.io/rzp/sFNXWkt"
    },
    "Startup India DPIIT Audit": {
        "price": "INR 18,000",
        "link": "https://rzp.io/rzp/sFNXWkt"
    }
}

ALL_KNOWN_SERVICES = {**CORRECT_LINKS, **SECONDARY_SERVICES}

print("=== START COMPREHENSIVE CODEBASE AUDIT ===")

anomalies = []

# Helper to find all occurrences of pattern and return context
def find_patterns_with_context(content, pattern):
    matches = []
    for m in re.finditer(pattern, content):
        start = max(0, m.start() - 60)
        end = min(len(content), m.end() + 60)
        matches.append((m.group(0), content[start:end].replace('\n', ' ')))
    return matches

for file_name in html_files:
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check 1: Hardcoded full domain URLs
    hardcoded_urls = re.findall(r'href=["\'](https?://(?:www\.)?vextaudit\.com/[^\s"\']+)["\']', content)
    if hardcoded_urls:
        anomalies.append({
            "file": file_name,
            "type": "hardcoded_url",
            "details": f"Found hardcoded domain URLs: {list(set(hardcoded_urls))}"
        })
        
    # Check 2: Razorpay links verification
    rzp_links_found = re.findall(r'https?://rzp\.io/rzp/\w+', content)
    for l in set(rzp_links_found):
        matched_svc = None
        for svc_name, svc_info in ALL_KNOWN_SERVICES.items():
            if svc_info["link"] == l:
                matched_svc = svc_name
                break
                
        if not matched_svc:
            anomalies.append({
                "file": file_name,
                "type": "unrecognized_razorpay_link",
                "details": f"Unrecognized link '{l}' found. Verify if it matches verified list."
            })

    # Check 3: Outdated export/FEMA compliance pricing (INR 35,000 is now INR 20,000/25,000)
    if "export" in file_name or file_name == "onboard.html":
        if "35,000" in content or "35K" in content:
            contexts = find_patterns_with_context(content, r'35,000|35\s*K')
            for p, ctx in contexts:
                anomalies.append({
                    "file": file_name,
                    "type": "outdated_pricing_text",
                    "details": f"Outdated pricing text '{p}' for export/FEMA compliance. Context: '... {ctx} ...'"
                })

    # Check 4: Check placeholder contact info
    if "Rayan" in content or "502-260-3057" in content or "260-3057" in content:
        contexts = find_patterns_with_context(content, r'Rayan|\+1|502')
        for p, ctx in contexts:
            anomalies.append({
                "file": file_name,
                "type": "placeholder_contact_info",
                "details": f"Placeholder contact '{p}' found in context: '... {ctx} ...'"
            })

    if "5724222727382" in content and file_name != "delivery.html": # delivery.html has it in cf-email
        anomalies.append({
            "file": file_name,
            "type": "placeholder_number",
            "details": f"Placeholder number '5724222727382' found."
        })

print(f"Total anomalies found: {len(anomalies)}\n")
for idx, a in enumerate(anomalies, 1):
    print(f"[{idx}] File: {a['file']} | Type: {a['type']}")
    print(f"    Details: {a['details']}")
    print("-" * 80)
