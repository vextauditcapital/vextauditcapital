import os
import re

directory = '.'
extensions = ('.html', '.js', '.py', '.md', '.json', '.txt')

replacements = [
    (r'', ''),
    (r'', ''),
    (r', ', ''),
    (r' \(\)', ''),
    (r' \(\)', ''),
    (r'', ''),
    (r'', '')
]

count = 0
for root, _, files in os.walk(directory):
    # skip .git and other hidden dirs
    if '.git' in root or 'venv' in root or '__pycache__' in root:
        continue
    for file in files:
        if file.endswith(extensions):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                for pattern, replacement in replacements:
                    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                
                # Cleanup some potential leftover punctuation like "Vext Audit Capital ." or "Vext Audit Capital"
                content = content.replace('Vext Audit Capital', 'Vext Audit Capital')
                content = content.replace('Vext Audit Capital', 'Vext Audit Capital')
                
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated: {filepath}")
                    count += 1
            except Exception as e:
                print(f"Failed to process {filepath}: {e}")

print(f"Total files updated: {count}")
