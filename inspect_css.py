import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's search for CSS files imported
links = re.findall(r'<link[^>]*href="([^"]+)"', text)
print("Imported links:", links)

# Let's find any inline style tag content
styles = re.findall(r'<style>(.*?)</style>', text, re.DOTALL)
print(f"Number of inline <style> tags: {len(styles)}")
for idx, style in enumerate(styles):
    print(f"Style tag {idx+1} length: {len(style)} chars")
