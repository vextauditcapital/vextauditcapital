import re

file_path = r"C:\Users\shyam\.gemini\antigravity\scratch\index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Search for headers or keywords related to "How We Work", "Process", "Pipeline", "Steps"
matches = re.findall(r'.{0,100}how we work.{0,150}', content, re.IGNORECASE)
for m in matches:
    print("Match:", m.strip())

# Search for "Welcome Email", "SOW", "Zoho" in index.html to see if it's there
zoho_matches = re.findall(r'.{0,100}zoho.{0,100}', content, re.IGNORECASE)
print("\nZoho matches in index.html:")
for zm in zoho_matches:
    print("  ", zm.strip())
