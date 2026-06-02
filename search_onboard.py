with open(r"C:\Users\shyam\.gemini\antigravity\scratch\onboard.html", 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'web3forms' in line.lower() or 'fetch(' in line:
        print(f"Line {idx+1}: {line.strip()}")
