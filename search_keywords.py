import os

def search_files():
    keywords = ["supabase", "fastapi", "cloud run", "secretmanager", "psycopg2"]
    found = {}
    for root, dirs, files in os.walk(r"C:\Users\shyam\.gemini\antigravity\scratch"):
        for file in files:
            if file.endswith((".py", ".js", ".sh", ".json", ".md", ".html", ".gs")):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for kw in keywords:
                            if kw in content.lower():
                                if kw not in found:
                                    found[kw] = []
                                found[kw].append(path)
                except Exception as e:
                    pass
    
    for kw, paths in found.items():
        print(f"Keyword '{kw}' found in:")
        for p in paths[:5]:
            print(f"  - {p}")
        if len(paths) > 5:
            print(f"  - and {len(paths)-5} more files")

if __name__ == "__main__":
    search_files()
