import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

for file_name in sorted(html_files):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        if 'rzp.io' in line or 'razorpay' in line.lower():
            # Print file name, line number, and content
            print(f"{file_name}:{idx+1}: {line.strip()}")
