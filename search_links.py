import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

print(f"Scanning {len(html_files)} HTML files...\n")

rzp_regex = re.compile(r'rzp\.io/rzp/\w+')
web3_regex = re.compile(r'access_key\s*,\s*[\'"][^\'"]+[\'"]')
email_regex = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
phone_regex = re.compile(r'\+?\d{1,3}[ \.-]?\(?\d{3}\)?[ \.-]?\d{3}[ \.-]?\d{4}')

for file_name in html_files:
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    rzp_matches = rzp_regex.findall(content)
    web3_matches = web3_regex.findall(content)
    email_matches = email_regex.findall(content)
    phone_matches = phone_regex.findall(content)
    
    if rzp_matches or web3_matches or email_matches or phone_matches:
        print(f"=== File: {file_name} ===")
        if rzp_matches:
            print("  Razorpay Links:")
            for m in set(rzp_matches):
                print(f"    - https://{m}")
        if web3_matches:
            print("  Web3Forms Keys:")
            for m in set(web3_matches):
                print(f"    - {m}")
        if email_matches:
            print("  Emails:")
            for m in set(email_matches):
                if not m.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                    print(f"    - {m}")
        if phone_matches:
            print("  Phones/Numbers:")
            for m in set(phone_matches):
                print(f"    - {m}")
        print()
