import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"

for root, dirs, files in os.walk(dir_path):
    for file_name in files:
        if file_name.endswith('.git') or '.git' in root:
            continue
        file_path = os.path.join(root, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Search for various pieces of the phrase
            terms = ['usd pricing', 'custom bundles', 'international clients', 'bundles on request', 'custom bundle']
            for term in terms:
                if term in content.lower():
                    # find line number
                    lines = content.split('\n')
                    for idx, line in enumerate(lines):
                        if term in line.lower():
                            print(f"FOUND '{term}' in {file_name}:{idx+1}: {line.strip()}")
        except Exception as e:
            pass
