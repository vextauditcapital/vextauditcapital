import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

search_dir = r"C:\Users\shyam\.gemini\antigravity\scratch"
terms = [
    r"audit\s+firm",
    r"auditing\s+firm",
    r"ca\s+firm",
    r"chartered\s+accountant",
    r"accounting\s+firm",
    r"audit\s+professional",
    r"legal\s+audit",
    r"ca\s+professional",
    r"auditor\s+professional",
]

compiled_terms = [re.compile(term, re.IGNORECASE) for term in terms]

results = []

for root, dirs, files in os.walk(search_dir):
    # Skip standard hidden/cache/scratch dirs
    # If the root starts with our specific scratch subfolder, skip it
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
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    for term_re in compiled_terms:
                        if term_re.search(line):
                            results.append({
                                "file": os.path.relpath(file_path, search_dir),
                                "line_num": i + 1,
                                "term": term_re.pattern,
                                "content": line.strip()
                            })
            except Exception as e:
                pass

output_path = os.path.join(search_dir, "scratch", "search_results.txt")
with open(output_path, "w", encoding="utf-8") as out:
    out.write(f"Found {len(results)} matches:\n")
    for r in sorted(results, key=lambda x: (x['file'], x['line_num'])):
        out.write(f"{r['file']}:{r['line_num']} [{r['term']}] -> {r['content']}\n")

print(f"Written {len(results)} matches to {output_path}")
for r in results[:15]:
    print(f"{r['file']}:{r['line_num']} -> {r['content'][:120]}")
