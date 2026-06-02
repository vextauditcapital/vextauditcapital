import glob
import re
import os

rupee = '\u20b9'

html_files = glob.glob('*.html')

for filepath in html_files:
    # Read ignoring encoding errors just in case, but write cleanly
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Fix the generic ? that are actually rupees.
    # We can use regex to find ? followed by digits and a comma.
    # e.g. "?18,000" -> "₹18,000"
    content = re.sub(r'\?(\d{2,3},\d{3})', f'{rupee}\\1', content)
    content = re.sub(r'\?(\d\.\d[L|M])', f'{rupee}\\1', content) # for ?1.5L
    
    # Fix "Rs." if any
    content = re.sub(r'Rs\.?\s*(\d{2,3},\d{3})', f'{rupee}\\1', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Corruption fixed.")