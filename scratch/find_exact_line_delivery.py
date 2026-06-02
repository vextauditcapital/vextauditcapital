with open(r"C:\Users\shyam\.gemini\antigravity\scratch\delivery.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    if "USD pricing" in line or "USD pricing is available" in line:
        print(f"Line {idx}: {line.strip()}")
