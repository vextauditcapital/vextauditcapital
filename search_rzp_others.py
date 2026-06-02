import os

search_dir = r"C:\Users\shyam\.gemini\antigravity\scratch"
results = []

for filename in os.listdir(search_dir):
    if filename.endswith(".html") and filename != "onboard.html":
        filepath = os.path.join(search_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if "rzp.io/rzp" in line or "rzp" in line:
                    results.append(f"{filename}:{i+1}: {line.strip()}")

print(f"Found {len(results)} occurrences of rzp in other html files:")
for r in results:
    print(r)
