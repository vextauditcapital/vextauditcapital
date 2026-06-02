import os
import re
import json

# Define colors for CLI report
class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(f"{colors.HEADER}{colors.BOLD}======================================================================")
print("             VEXT AUDIT CAPITAL - AUTOMATED SYSTEM AUDIT SCANNER")
print(f"======================================================================{colors.ENDC}")
print(f"{colors.CYAN}Project Root:{colors.ENDC} {PROJECT_ROOT}\n")

files_to_scan = [
    "agents/config.py",
    "agents/lead_command.py",
    "agents/run_all_agents.py",
    "agents/vetting_agent.py",
    "agents/email_command.py",
    "agents/utils/security_vault.py",
    "agents/utils/analytics.py",
    "agents/utils/invoice_agent.py",
    "agents/utils/pdf_report_generator.py",
    "agents/utils/telemetry.py",
    "agents/utils/gcp_secrets.py",
    "app/main.py",
    "app/database.py",
    "app/models.py",
    "ecosystem.config.js"
]

violations = []

for rel_path in files_to_scan:
    abs_path = os.path.join(PROJECT_ROOT, rel_path)
    if not os.path.exists(abs_path):
        print(f"{colors.WARNING}[SKIP] File not found:{colors.ENDC} {rel_path}")
        continue
        
    print(f"{colors.BLUE}[SCAN] Reviewing file:{colors.ENDC} {rel_path}")
    
    with open(abs_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines):
        line_num = idx + 1
        
        # 1. Absolute Windows local paths
        if "C:\\Users\\" in line or "C:\\" in line or r"C:\Users" in line:
            # Skip if it is in comment and not code, but scan strictly
            violations.append({
                "file": rel_path,
                "line": line_num,
                "type": "ABSOLUTE_PATH",
                "severity": "CRITICAL_BLOCKER",
                "snippet": line.strip(),
                "description": "Hardcoded absolute local development Windows path. Will crash on Linux/Docker."
            })
            
        # 2. Hardcoded GWorkspace Gmail App Passwords
        if "PASS_" in line and "Field(default=" in line and "MOCK_PASSWORD" not in line and "placeholder" not in line:
            # Extract password
            violations.append({
                "file": rel_path,
                "line": line_num,
                "type": "HARDCODED_PASSWORD",
                "severity": "CRITICAL_LEAKAGE",
                "snippet": line.strip(),
                "description": "Plaintext Google Workspace App Password default value. Violates SOC 2 and GDPR."
            })
            
        # 3. Status color typo in telemetry
        if "status_color" in line:
            violations.append({
                "file": rel_path,
                "line": line_num,
                "type": "TELEMETRY_TYPO",
                "severity": "CRITICAL_ERROR",
                "snippet": line.strip(),
                "description": "Attribute 'status_color' does not exist on requests 'Response'. Will crash telemetry alerts."
            })
            
        # 4. JSON parse unsafe get
        if rel_path == "app/main.py" and "data.get(" in line and line_num < 140:
            # Check if we have safety verification before
            with open(abs_path, "r", encoding="utf-8") as f2:
                content = f2.read()
            if "isinstance(data, dict)" not in content:
                violations.append({
                    "file": rel_path,
                    "line": line_num,
                    "type": "UNSAFE_INTAKE_PAYLOAD",
                    "severity": "HIGH_VULNERABILITY",
                    "snippet": line.strip(),
                    "description": "Accesses keys of parsed JSON object directly without verifying if payload is a dict. Will raise unhandled AttributeError (500) if payload is an array or primitive."
                })

print("\n" + "="*70)
print(f"{colors.HEADER}{colors.BOLD}                           AUDIT SCAN SUMMARY{colors.ENDC}")
print("="*70)

if not violations:
    print(f"{colors.GREEN}✔ Zero violations detected! The codebase conforms with portability, security, and safety guidelines.{colors.ENDC}")
else:
    print(f"{colors.FAIL}Found {len(violations)} security vulnerabilities, portability blockers, or architectural loop holes:{colors.ENDC}\n")
    for v in violations:
        sev_color = colors.FAIL if "CRITICAL" in v["severity"] else colors.WARNING
        print(f"[{sev_color}{v['severity']}{colors.ENDC}] {colors.BOLD}{v['file']}:{v['line']}{colors.ENDC}")
        print(f"  {colors.CYAN}Type:{colors.ENDC} {v['type']}")
        print(f"  {colors.CYAN}Issue:{colors.ENDC} {v['description']}")
        print(f"  {colors.CYAN}Code:{colors.ENDC} `{v['snippet']}`")
        print("-" * 50)

print(f"\n{colors.HEADER}{colors.BOLD}======================================================================{colors.ENDC}")
