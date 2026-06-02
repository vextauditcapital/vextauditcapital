import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find all divs with class="service-card" or similar
# A service card looks like:
# <div class="service-card ...">
#   ...
#   <h3 class="service-title">...</h3>
#   ...
#   <a href="..." class="service-cta">Explore Details</a>
# </div>

# Let's split content by '<div class="service-card'
blocks = content.split('<div class="service-card')
print(f"Split index.html into {len(blocks)} blocks")

for idx, block in enumerate(blocks[1:], 1):
    # Find title
    title_m = re.search(r'<h3 class="service-title">(.*?)</h3>', block)
    title = title_m.group(1) if title_m else "No Title"
    
    # Find link
    link_m = re.search(r'href=["\'](.*?)["\']', block)
    link = link_m.group(1) if link_m else "No Link"
    
    print(f"{idx:2d}. Service: {title:50} | Link: {link}")
