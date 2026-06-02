with open(r"C:\Users\shyam\.gemini\antigravity\scratch\onboard.html", 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if 'CRM_CONFIG' in line:
            print(f"Line {idx+1}: {line.strip()}")
