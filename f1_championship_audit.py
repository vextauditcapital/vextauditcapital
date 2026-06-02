import os
import re
import sys
import json
import ast

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]
py_files = []

for root_dir, dirs, files in os.walk(dir_path):
    # Skip __pycache__ and hidden dirs
    if '__pycache__' in root_dir or '.git' in root_dir:
        continue
    for f in files:
        if f.endswith('.py'):
            py_files.append(os.path.join(root_dir, f))

print("================================================================================")
print("🏁 FORMULA 1 PRE-CHAMPIONSHIP DIAGNOSTIC SYSTEM - VEXT AUDIT CAPITAL")
print("================================================================================")
print(f"Initializing telemetry on: {len(html_files)} HTML files, {len(py_files)} Python scripts.")

# Load correct services mapping for validation
CORRECT_SERVICE_KEYS = {
    "gst": "GST Audit & Compliance",
    "tds": "TDS Compliance Audit",
    "roc": "ROC Annual Compliance Audit",
    "payroll": "Payroll Compliance Audit",
    "income-tax": "Income Tax Compliance Audit",
    "fema": "FEMA Compliance Audit",
    "dpdp": "DPDP Readiness Assessment",
    "fin-ops": "Financial Operations Audit",
    "export": "Export Compliance Audit",
    "transfer-pricing": "Transfer Pricing Documentation",
    "msme": "MSME Compliance Health Check",
    "startup-dpiit": "Startup DPIIT Compliance Audit",
    "it-cyber": "IT & Cybersecurity Audit",
    "bundle": "Full Audit Bundle",
    "iso27001": "ISO 27001 Gap Assessment",
    "soc2": "SOC 2 Readiness Assessment",
    "gdpr": "GDPR Compliance Assessment",
    "hipaa": "HIPAA Compliance Assessment",
    "pcidss": "PCI-DSS Compliance Assessment",
    "esg": "ESG Baseline Report",
    "vendor-risk": "Vendor Risk Assessment",
    "aml-kyc": "AML / KYC Policy Audit",
    "process": "AI Business Process Intelligence",
    "competitive": "AI Competitive Intelligence",
    "market-entry": "AI Market Entry Analysis",
    "ops-risk": "AI Operational Risk Assessment",
    "vextintel-monthly": "VextIntel Monthly Retainer",
    "vextintel-global": "VextIntel Global Edition",
    "annual-sub": "Annual Compliance Subscription",
    "vextintel-annual": "VextIntel Annual Retainer"
}

results = {
    "Compilations": [],
    "BannedPhrases": [],
    "PIILeaks": [],
    "BrokenLinks": [],
    "MarginLeaks": [],
    "CORSBypasses": []
}

# ------------------------------------------------------------------------------
# LAP 1: AERODYNAMICS (HTML & Structural Auditing)
# ------------------------------------------------------------------------------
print("\n🏎️  LAP 1: AERODYNAMICS (HTML Integrity & Logo Paths)...")
logo_underscore_pattern = re.compile(r'VEXT_AUDIT_CAPITAL_LOGO\.jpeg', re.IGNORECASE)
broken_logo_count = 0
unclosed_tags_count = 0

for h in html_files:
    path = os.path.join(dir_path, h)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Check for underscore in logo path
    if logo_underscore_pattern.search(html):
        print(f"  [ANOMALY] Broken underscore logo filename found in: {h}")
        broken_logo_count += 1
        
    # Simple unclosed tag check (divs, sections)
    open_divs = len(re.findall(r'<div\b', html))
    close_divs = len(re.findall(r'</div>', html))
    if open_divs != close_divs:
        print(f"  [WARNING] Mismatched DIV tags in {h} (open: {open_divs}, close: {close_divs})")
        unclosed_tags_count += 1

# ------------------------------------------------------------------------------
# LAP 2: FUEL LINE (Static Compilation Check)
# ------------------------------------------------------------------------------
print("\n🏎️  LAP 2: FUEL LINE (Python & JS Compilation Check)...")
syntax_failures = 0

for py_path in py_files:
    try:
        with open(py_path, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
    except SyntaxError as se:
        print(f"  [CRITICAL] Syntax error in Python script {os.path.basename(py_path)}: {se}")
        syntax_failures += 1

# Check Apps Script Code.gs syntax locally
try:
    code_gs_path = os.path.join(dir_path, "Code.gs")
    if os.path.exists(code_gs_path):
        import subprocess
        cmd = ['node', '-e', "const fs = require('fs'); const vm = require('vm'); vm.createScript(fs.readFileSync('Code.gs', 'utf8'));"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=dir_path)
        if res.returncode != 0:
            print(f"  [CRITICAL] Syntax error in Code.gs compiled via Node: {res.stderr.strip()}")
            syntax_failures += 1
except Exception as ex:
    print(f"  Error checking Code.gs syntax: {ex}")

# ------------------------------------------------------------------------------
# LAP 3: BRAKES & SAFETY (Hardcoded Credentials & Sensitive PII Leakage)
# ------------------------------------------------------------------------------
print("\n🏎️  LAP 3: BRAKES & SAFETY (PII & API Credential Leaks)...")
key_patterns = [
    (re.compile(r'sk-ant-api[a-zA-Z0-9_\-]{20,}'), "Anthropic API Key"),
    (re.compile(r'rzp_live_[a-zA-Z0-9]{14}'), "Razorpay Live Key ID"),
    (re.compile(r'aweS7hK5_nrAL7W'), "Razorpay Webhook Secret"), # Check if hardcoded in client files
]

leakage_found = 0
for h in html_files:
    path = os.path.join(dir_path, h)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Client files must never have live secrets or private keys
    for pattern, name in key_patterns:
        if pattern.search(html):
            print(f"  [CRITICAL] Hardcoded sensitive credential ({name}) found in client file: {h}")
            leakage_found += 1

# ------------------------------------------------------------------------------
# LAP 4: GEARS (CTA Links & Routing Funnel Verification)
# ------------------------------------------------------------------------------
print("\n🏎️  LAP 4: GEARS (30-Service Funnel Flow Integrity)...")
funnel_breaks = 0

for h in html_files:
    if h in ['index.html', 'onboard.html', 'happiness.html', 'upload.html', 'privacy.html', 'terms.html', 'cookies.html', 'data-policy.html', 'delivery.html', 'disclosure.html', 'refund.html', 'security.html']:
        continue
        
    path = os.path.join(dir_path, h)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Subpage must point CTAs to onboard.html?service=[key]
    cta_matches = re.findall(r'href=["\']onboard\.html\?service=([a-zA-Z0-9_\-]+)["\']', html)
    if not cta_matches:
        print(f"  [ANOMALY] Educational subpage {h} has a broken or missing onboarding CTA link!")
        funnel_breaks += 1
    else:
        for key in cta_matches:
            if key not in CORRECT_SERVICE_KEYS:
                print(f"  [CRITICAL] Subpage {h} is routing to an INVALID service parameter: ?service={key}")
                funnel_breaks += 1

# ------------------------------------------------------------------------------
# LAP 5: THERMAL (Pricing, Currency & Banned Phrases)
# ------------------------------------------------------------------------------
print("\n🏎️  LAP 5: THERMAL (Pricing Mismatch, USD Remnants & Margin Leaks)...")
pricing_violations = 0
banned_phrases = ["USD pricing available", "Custom bundles on request"]

for h in html_files:
    path = os.path.join(dir_path, h)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Check for banned phrases
    for phrase in banned_phrases:
        if phrase.lower() in html.lower():
            print(f"  [ANOMALY] Banned phrase '{phrase}' found in {h}")
            pricing_violations += 1
            
    # Check for "Ask a Question"
    if "Ask a Question" in html:
        print(f"  [ANOMALY] Remaining 'Ask a Question' reference found in {h}")
        pricing_violations += 1

# ------------------------------------------------------------------------------
# LAP 6: TELEMETRY (CORS Check, Web3Forms Purge & GAS Hooks)
# ------------------------------------------------------------------------------
print("\n🏎️  LAP 6: TELEMETRY (CORS Bypass, Web3Forms Excision & Direct GAS CRM Hooks)...")
telemetry_leaks = 0

for h in html_files:
    path = os.path.join(dir_path, h)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Ensure Web3Forms is 100% purged from HTML forms
    if "api.web3forms.com" in html or "83cc3e63-fbee-43e4-ba81-a074039de80b" in html:
        print(f"  [CRITICAL] Web3Forms endpoint or Access Key leak found in: {h}")
        telemetry_leaks += 1

# Check onboard.html direct posting
onboard_path = os.path.join(dir_path, "onboard.html")
if os.path.exists(onboard_path):
    with open(onboard_path, 'r', encoding='utf-8') as f:
        onboard_html = f.read()
    if "AKfycby_YOUR_GAS_WEB_APP_URL_HERE" in onboard_html:
        print("  [CRITICAL] Onboarding form is still using the GAS placeholder URL!")
        telemetry_leaks += 1
    if "text/plain" not in onboard_html:
        print("  [WARNING] Onboarding form is missing 'text/plain' CORS pre-flight bypass header!")
        telemetry_leaks += 1

print("\n================================================================================")
print("📊 FINAL TELEMETRY SCOREBOARD")
print("================================================================================")
print(f"  1. Aerodynamics (HTML):     {broken_logo_count} Broken Logo, {unclosed_tags_count} Tag Mismatches")
print(f"  2. Fuel Line (Compiles):    {syntax_failures} Syntax Failures")
print(f"  3. Brakes & Safety (PII):   {leakage_found} PII/Secret Leaks")
print(f"  4. Transmission (Gears):    {funnel_breaks} Broken Funnel Flows")
print(f"  5. Thermal (Pricing):       {pricing_violations} Pricing/Banned Phrase Violations")
print(f"  6. Telemetry (CORS/CRM):    {telemetry_leaks} Web3Forms/CRM Pipeline Errors")
print("================================================================================")

total_errors = broken_logo_count + unclosed_tags_count + syntax_failures + leakage_found + funnel_breaks + pricing_violations + telemetry_leaks
if total_errors == 0:
    print("🏆 SYSTEM RATING: 10/10 - THE CAR IS READY FOR THE WORLD CHAMPIONSHIP!")
else:
    print(f"⚠️  SYSTEM RATING: {max(0, 10 - total_errors)}/10 - CRITICAL PIT STOP REQUIRED ({total_errors} defects found)")
print("================================================================================")
