import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# We can split the text by '<div class="service-card'
blocks = text.split('<div class="service-card')
print(f"Total service-card blocks: {len(blocks)-1}")

for idx, block in enumerate(blocks[1:]):
    # This block represents one card
    # Let's find the title
    title_m = re.search(r'<h3 class="service-title">([^<]+)</h3>', block)
    title = title_m.group(1).strip() if title_m else "UNKNOWN"
    
    # Let's find the first href in this block
    # Since it's split on service-card, the first href in this block should belong to this card
    href_m = re.search(r'href="([^"]+)"', block)
    href = href_m.group(1).strip() if href_m else "NONE"
    
    print(f"Card {idx+1:2d}. Title: '{title}' | Link: '{href}'")
