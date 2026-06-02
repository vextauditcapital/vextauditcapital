import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

replacements = [
    # Order matters: replace longer patterns first
    (r'href="/onboard\?service=([\w-]+)"', r'href="onboard.html?service=\1"'),
    (r'href="/onboard"', r'href="onboard.html"'),
    (r'href="/privacy"', r'href="privacy.html"'),
    (r'href="/terms"', r'href="terms.html"'),
    (r'href="/refund"', r'href="refund.html"'),
    (r'href="/delivery"', r'href="delivery.html"'),
    (r'href="/data-policy"', r'href="data-policy.html"'),
    (r'href="/cookies"', r'href="cookies.html"'),
    (r'href="/security"', r'href="security.html"'),
    (r'href="/disclosure"', r'href="disclosure.html"'),
    (r'href="/#services"', r'href="index.html#services"'),
    (r'href="/#pricing"', r'href="index.html#pricing"'),
    (r'href="/#about"', r'href="index.html#about"'),
    (r'href="/#vextintel"', r'href="index.html#vextintel"'),
    (r'href="/#contact"', r'href="index.html#contact"'),
    (r'href="/"', r'href="index.html"'),
    (r'src="/VEXT-AUDIT-CAPITAL-LOGO\.jpg"', r'src="VEXT-AUDIT-CAPITAL-LOGO.jpg"'),
    (r'src="/VEXT-AUDIT-CAPITAL-LOGO\.jpeg"', r'src="VEXT-AUDIT-CAPITAL-LOGO.jpeg"'),
]

print(f"Modifying {len(html_files)} HTML files to use relative links...\n")

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    original_content = content
    
    for pattern, repl in replacements:
        new_content, count = re.subn(pattern, repl, content)
        if count > 0:
            content = new_content
            modified = True
            
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  - Modified: {file_name}")
    else:
        print(f"  - No changes needed: {file_name}")

print("\nLink refactoring completed successfully!")
