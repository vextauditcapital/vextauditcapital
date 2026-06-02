import os
import re

search_dir = r"C:\Users\shyam\.gemini\antigravity\scratch"
patterns = {
    "USD pricing": re.compile(r"USD pricing", re.IGNORECASE),
    "Custom bundle": re.compile(r"Custom bundle", re.IGNORECASE),
    "international clients": re.compile(r"international clients", re.IGNORECASE),
    "on request": re.compile(r"on request", re.IGNORECASE),
    "USD": re.compile(r"\bUSD\b"),
    "dollar": re.compile(r"\bdollar\b", re.IGNORECASE),
    "\$": re.compile(r"\$")
}

matches = []
for filename in os.listdir(search_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(search_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.splitlines()
        for i, line in enumerate(lines):
            # Check for matches
            for key, pattern in patterns.items():
                if pattern.search(line):
                    # Exclude the HHS statistic in hipaa-compliance-assessment.html
                    if filename == "hipaa-compliance-assessment.html" and "$1 million" in line:
                        continue
                    matches.append(f"{filename}:{i+1} [{key}]: {line.strip()}")

print(f"Found {len(matches)} matches:")
with open("deep_search_results.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(matches))

for m in matches[:40]:
    print(m)
if len(matches) > 40:
    print(f"... and {len(matches)-40} more matches.")
