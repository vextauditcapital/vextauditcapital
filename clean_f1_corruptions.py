import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
corrupted_files = [
    'dpdp-readiness-assessment.html',
    'export-compliance.html',
    'financial-operations-audit.html',
    'gst-audit-compliance.html',
    'it-cybersecurity-audit.html',
    'vextintel-monthly-retainer.html'
]

print("Running advanced structural tag cleanup...")

for filename in corrupted_files:
    path = os.path.join(dir_path, filename)
    if not os.path.exists(path):
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the first extra </div> after audit-grid
    pattern_after_audit = re.compile(
        r'</div>\s*</div>\s*<h3 style="font-family:var\(--ff-d\);font-size:18px;color:var\(--cream\);letter-spacing:0\.05em;margin:32px 0 18px;" class="fade-up">What You Receive</h3>',
        re.DOTALL
    )
    content, count_audit_div = pattern_after_audit.subn(
        '</div>\n      <h3 style="font-family:var(--ff-d);font-size:18px;color:var(--cream);letter-spacing:0.05em;margin:32px 0 18px;" class="fade-up">What You Receive</h3>',
        content
    )

    # 2. Replace the second extra </div> after del-list
    pattern_after_del = re.compile(
        r'</div>\s*</div>\s*</div>\s*<div class="svc-sidebar">',
        re.DOTALL
    )
    content, count_del_div = pattern_after_del.subn(
        '</div>\n    </div>\n    <div class="svc-sidebar">',
        content
    )

    if count_audit_div or count_del_div:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [SUCCESS] Cleaned extra DIVs in {filename}: post-audit ({count_audit_div}), post-del ({count_del_div}).")
    else:
        print(f"  [WARNING] No extra DIVs matched in {filename}.")

print("Advanced DIV cleanup complete!")
