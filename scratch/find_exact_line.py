with open(r"C:\Users\shyam\.gemini\antigravity\scratch\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    if "USD pricing available" in line:
        print(f"Line {idx}: {line.strip()}")
