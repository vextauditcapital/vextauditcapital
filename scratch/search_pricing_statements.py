import os
import re

directory = r"C:\Users\shyam\.gemini\antigravity\scratch"
search_phrases = [
    r"USD pricing available",
    r"international clients",
    r"custom bundles",
    r"discrimination",
    r"on request",
    r"USD pricing",
    r"behavioral"
]

results = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".html") or file.endswith(".md"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                for phrase in search_phrases:
                    matches = list(re.finditer(phrase, content, re.IGNORECASE))
                    if matches:
                        for match in matches:
                            # get some context around the match
                            start = max(0, match.start() - 60)
                            end = min(len(content), match.end() + 60)
                            snippet = content[start:end].replace("\n", " ")
                            results.append({
                                "file": file,
                                "phrase": phrase,
                                "snippet": snippet
                            })
            except Exception as e:
                pass

print(f"Found {len(results)} matches:")
for r in results:
    print(f"File: {r['file']} | Phrase: {r['phrase']}")
    print(f"  Snippet: ... {r['snippet'].strip()} ...")
