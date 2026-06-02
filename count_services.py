import os
import re

dir_path = r"C:\Users\shyam\.gemini\antigravity\scratch"
index_path = os.path.join(dir_path, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find service cards
# Each service card looks like:
# <div class="service-card ...">
# ...
# <h3 class="service-title">...</h3>
# ...
# <a href="..." ...>...</a>
# </div>

# We can find all class="service-title" and see their names and preceding href or succeeding href
titles = re.findall(r'<h3 class="service-title">([^<]+)</h3>', content)
links = re.findall(r'href="([^"]+)" class="service-cta"', content)

print(f"Total titles found: {len(titles)}")
print(f"Total links found: {len(links)}")

# Let's search card blocks to match them
cards = re.findall(r'<div class="service-card[^"]*">.*?<h3 class="service-title">([^<]+)</h3>.*?href="([^"]+)"', content, re.DOTALL)
print(f"Total matched cards: {len(cards)}")
for idx, (title, href) in enumerate(cards):
    print(f"{idx+1:2d}. Title: '{title.strip()}', Link: '{href.strip()}'")
