import os

# Let's search all markdown, text, or python files in the directory for lists of services and rzp.io links
files = [f for f in os.listdir('.') if f.endswith('.md') or f.endswith('.txt') or f.endswith('.py')]

for fname in files:
    if fname == 'search_links_onboard.py' or fname == 'search_rzp_all.py':
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'MyIHpEhi' in content or 'A98OOcD' in content:
        print(f"File {fname} contains matching payment links.")
        # Find lines with rzp.io
        lines = content.split('\n')
        for idx, line in enumerate(lines, 1):
            if 'rzp.io' in line:
                print(f"  Line {idx:3d}: {line[:120]}")
