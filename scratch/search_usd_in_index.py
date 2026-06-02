import os

file_path = r"C:\Users\shyam\.gemini\antigravity\scratch\index.html"
with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

lines = content.split('\n')
for idx, line in enumerate(lines):
    if "usd" in line.lower() or "custom" in line.lower():
        print(f"Line {idx+1}: {line.strip()}")
