import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
for f_name in os.listdir(dir_path):
    if f_name.endswith('.html'):
        path = os.path.join(dir_path, f_name)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "Statement of Work" in content or "SOW" in content:
            print(f"File: {f_name}")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "Statement of Work" in line or "SOW" in line or "Zoho Sign" in line:
                    print(f"  {i+1}: {line.strip()}")
