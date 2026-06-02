import os

search_dir = r"C:\Users\shyam\.gemini\antigravity\scratch"
results = []

for filename in os.listdir(search_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(search_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if "$" in line:
                        results.append(f"{filename}:{i+1}: {line.strip()}")
        except Exception as e:
            results.append(f"Error reading {filename}: {str(e)}")

output_path = os.path.join(search_dir, "scratch_dollar_matches.txt")
with open(output_path, "w", encoding="utf-8") as out:
    out.write("\n".join(results))

print(f"Dollar search complete. Found {len(results)} matches. Results written to {output_path}")
