import os
import re

# Define files to fix and their mapping of old to new price strings
fixes = {
    "fema-compliance-audit.html": [
        ("Rs.35,000", "Rs.25,000"),
        ("Rs. 35,000", "Rs.25,000"),
        ("35,000 / review", "25,000 / review"),
        ("35,000", "25,000")
    ],
    "payroll-compliance-audit.html": [
        ("Rs.25,000", "Rs.22,000"),
        ("Rs. 25,000", "Rs.22,000"),
        ("25,000 / audit", "22,000 / audit"),
        ("25,000", "22,000")
    ],
    "startup-dpiit-compliance-audit.html": [
        ("Rs.12,000", "Rs.18,000"),
        ("Rs. 12,000", "Rs.18,000"),
        ("12,000 / assessment", "18,000 / assessment"),
        ("12,000", "18,000")
    ],
    "annual-compliance-subscription.html": [
        ("Rs.1,20,000", "Rs.60,000"),
        ("Rs. 1,20,000", "Rs.60,000"),
        ("1,20,000 / year", "60,000 / year"),
        ("1,20,000", "60,000")
    ]
}

print("Starting landing pages pricing updates...")

for file_name, replacements in fixes.items():
    if not os.path.exists(file_name):
        print(f"WARNING: File {file_name} does not exist.")
        continue
        
    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read()
        
    updated_content = content
    for old, new in replacements:
        updated_content = updated_content.replace(old, new)
        
    if updated_content != content:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"SUCCESS: Updated pricing in {file_name}.")
    else:
        print(f"INFO: No updates needed for {file_name}.")

print("Landing pages pricing updates complete.")
