import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = []

for root, dirs, files in os.walk(dir_path):
    # Skip .git and __pycache__
    if '.git' in dirs:
        dirs.remove('.git')
    if '__pycache__' in dirs:
        dirs.remove('__pycache__')
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.relpath(os.path.join(root, file), dir_path))

print(f"Found {len(html_files)} HTML files recursively:")
for f in sorted(html_files):
    print(f"  - {f}")
