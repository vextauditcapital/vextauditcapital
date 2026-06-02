import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

target_strings = [
    "USD pricing available for international clients",
    "Custom bundles on request",
    "USD pricing",
    "Custom bundles",
    "rzp.io/rzp"
]

results = []
for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        for target in target_strings:
            if target.lower() in line.lower():
                results.append(f"{file_name}:{idx+1} ({target}): {line.strip()}")

output_path = os.path.join(dir_path, "search_results_output.txt")
with open(output_path, 'w', encoding='utf-8') as out:
    out.write("\n".join(results))

print(f"Done. Found {len(results)} matches. Saved to search_results_output.txt")
