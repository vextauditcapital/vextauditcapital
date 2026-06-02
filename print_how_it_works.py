import re

file_path = r"C:\Users\shyam\.gemini\antigravity\scratch\index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find the "How We Work" section. We'll search for 'How We Work' and print around it.
pos = content.find("How We Work")
if pos != -1:
    print(content[pos-200:pos+3000])
else:
    print("Not found.")
