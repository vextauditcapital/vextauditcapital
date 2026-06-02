from bs4 import BeautifulSoup
import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Find all cards
cards = soup.find_all(class_=re.compile(r"service-card"))
print(f"BeautifulSoup found {len(cards)} service cards.")

# Let's check how many cards are top-level inside their grid, or nested
for idx, card in enumerate(cards):
    parent = card.parent
    parent_classes = parent.get("class", []) if parent else []
    parent_id = parent.get("id", "") if parent else ""
    # Check parent's parent
    grandparent = parent.parent if parent else None
    grandparent_classes = grandparent.get("class", []) if grandparent else []
    
    title = card.find(class_="service-title")
    title_text = title.get_text(strip=True) if title else "NO TITLE"
    
    print(f"Card {idx+1}: {title_text}")
    print(f"  Parent: tag={parent.name if parent else 'None'} classes={parent_classes} id={parent_id}")
    if grandparent:
        print(f"  Grandparent: tag={grandparent.name} classes={grandparent_classes}")
