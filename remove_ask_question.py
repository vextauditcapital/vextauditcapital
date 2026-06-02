import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

target_str = '<a href="mailto:support@vextaudit.com" class="btn-ghost">Ask a Question</a>'

modified_count = 0

for file_name in html_files:
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if target_str in content:
        # Let's replace the target string with an empty string
        # Also clean up any extra surrounding whitespace or newlines if needed,
        # but a clean string replacement is safest.
        new_content = content.replace(target_str, "")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Removed 'Ask a Question' button from: {file_name}")
        modified_count += 1

print(f"\nSuccessfully removed 'Ask a Question' button from {modified_count} files!")
