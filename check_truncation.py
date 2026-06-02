import os

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
html_files = [f for f in os.listdir(dir_path) if f.endswith('.html')]

print("Checking for unclosed or truncated HTML files...")

for file_name in html_files:
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        
    has_body_close = "</body>" in content or "</BODY>" in content
    has_html_close = "</html>" in content or "</HTML>" in content
    
    if not (has_body_close and has_html_close):
        print(f"Truncated file found: {file_name}")
        end_text = content[-100:].replace('\n', ' ')
        print(f"  - Ends with: {end_text}")
        print("-" * 50)
