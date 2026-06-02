import os

search_dir = r"C:\Users\shyam\.gemini\antigravity\scratch"

replacements = {
    "index.html": [
        ("CA-backed AI compliance audit", "expert-backed AI compliance audit"),
        ("CA-backed AI audit", "expert-backed AI compliance diagnostics")
    ],
    "update_homepage.py": [
        ("CA-backed AI compliance audit", "expert-backed AI compliance audit"),
        ("CA-backed AI audit", "expert-backed AI compliance diagnostics")
    ],
    "data-policy.html": [
        ("ICAI Data Standards", "AI Audit Standards"),
        ("ICAI standards", "regulatory standards"),
        ("ICAI and Income Tax Act", "Income Tax Act and industry standards")
    ],
    "delivery.html": [
        ("ICAI Standards", "Industry Best Practices")
    ],
    "privacy.html": [
        ("ICAI Standards", "AI Audit Standards"),
        ("ICAI standards, regulatory inquiry, or peer review", "regulatory inquiry, court orders, or compliance auditing mandates"),
        ("ICAI and Income Tax Act requirement", "Income Tax Act and standard corporate requirements"),
        ("ICAI professional standards, the GST Act 2017, and the LLP Act 2008", "corporate record retention guidelines, the GST Act 2017, and the LLP Act 2008")
    ],
    "refund.html": [
        ("ICAI Standards", "Industry Best Practices"),
        ("ICAI standard", "standard compliance framework")
    ],
    "security.html": [
        ("ICAI Standards", "Industry Best Practices")
    ],
    "terms.html": [
        ("ICAI Standards", "Industry Best Practices"),
        ("ICAI standard", "standard compliance framework"),
        ("ICAI standards, or peer review", "or regulatory inquiry"),
        ("The Firm maintains professional independence in all audit and assurance engagements in accordance with the ICAI Code of Ethics.", "The Firm maintains independence and objectivity in all compliance assessments."),
        ("The Client agrees to disclose any information that may affect the Firm's independence.", "The Client agrees to disclose any information that may affect the Firm's objectivity."),
        ("assessed against ICAI standards and applicable regulatory guidelines", "assessed against standard compliance audit practices and applicable regulatory guidelines")
    ]
}

modified_files = []

for rel_path, reps in replacements.items():
    file_path = os.path.join(search_dir, rel_path)
    if not os.path.exists(file_path):
        print(f"WARNING: File {rel_path} does not exist!")
        continue
        
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        modified_content = content
        changes_made = 0
        for target, replacement in reps:
            if target in modified_content:
                modified_content = modified_content.replace(target, replacement)
                changes_made += 1
                print(f"  [{rel_path}] Replaced '{target}' -> '{replacement}'")
            else:
                # Check case variations or partial matching
                print(f"  [{rel_path}] NOT FOUND: '{target}'")
                
        if changes_made > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(modified_content)
            modified_files.append(rel_path)
            print(f"SUCCESS: Updated {rel_path} with {changes_made} changes.")
        else:
            print(f"No changes made to {rel_path}.")
            
    except Exception as e:
        print(f"ERROR modifying {rel_path}: {e}")

print(f"\nCompleted legal reframing sweep. Updated {len(modified_files)} files: {modified_files}")
