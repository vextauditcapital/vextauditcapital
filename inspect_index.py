from bs4 import BeautifulSoup
import os

file_path = r"C:\Users\shyam\.gemini\antigravity\scratch\index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

links = soup.find_all('a')
print(f"Total links found in index.html: {len(links)}")
for i, link in enumerate(links):
    href = link.get('href', '')
    text = link.get_text().strip().replace('\n', ' ')
    if 'onboard' in href or 'rzp' in href:
        print(f"{i:3d}: text=\"{text[:50]}\", href=\"{href}\"")
