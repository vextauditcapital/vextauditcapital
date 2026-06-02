import os

search_dir = r"C:\Users\shyam\.gemini\antigravity\scratch"
results = []

for root, dirs, files in os.walk(search_dir):
    rel_root = os.path.relpath(root, search_dir)
    if rel_root != ".":
        parts = rel_root.split(os.sep)
        if any(p in {".git", "__pycache__", "node_modules", "scratch"} for p in parts):
            continue
            
    for file in files:
        if file.endswith((".html", ".py", ".md", ".txt")):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if "ICAI" in content:
                    # find line numbers
                    lines = content.splitlines()
                    for idx, line in enumerate(lines):
                        if "ICAI" in line:
                            results.append({
                                "file": os.path.relpath(file_path, search_dir),
                                "line_num": idx + 1,
                                "content": line.strip()
                            })
            except Exception as e:
                pass

print(f"Found {len(results)} matches for 'ICAI':")
for r in results:
    print(f"  {r['file']}:{r['line_num']} -> {r['content']}")
