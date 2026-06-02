import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # search case insensitively
    lines = content.split('\n')
    for idx, line in enumerate(lines):
        if 'usd pricing' in line.lower() or 'custom bundles on request' in line.lower() or 'custom bundles' in line.lower():
            print(f"MATCH in {file_name}:{idx+1}: {line.strip()}")
