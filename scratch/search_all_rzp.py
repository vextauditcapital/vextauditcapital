import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
for root, dirs, files in os.walk(dir_path):
    for f_name in files:
        if f_name.endswith(('.html', '.js', '.py')):
            path = os.path.join(root, f_name)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if "rzp.io" in content:
                    print(f"File: {path}")
            except Exception as e:
                pass
