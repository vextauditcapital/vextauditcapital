import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's extract each div with class "service-card"
# We can find all text between <div class="service-card and the next </div>, taking care of nesting
# Since check_html_nesting.py showed that each card starts at depth 1 and ends at depth 2 inside a flat container,
# we can grab from <div class="service-card... until the first closed </div>

cards_matches = re.finditer(r'<div class="service-card[^"]*"[^>]*>', text)
cards_list = list(cards_matches)

print(f"Total service cards found by regex: {len(cards_list)}")

for idx, match in enumerate(cards_list):
    start_pos = match.start()
    # Find the next </div> tag after this
    end_pos = text.find("</div>", start_pos)
    if end_pos != -1:
        card_content = text[start_pos:end_pos+6]
        
        title_m = re.search(r'<h3 class="service-title">(.*?)</h3>', card_content)
        title = title_m.group(1).strip() if title_m else "UNKNOWN TITLE"
        
        # Let's check for any display:none or inline styles or hidden class
        classes_m = re.search(r'class="([^"]+)"', card_content)
        classes = classes_m.group(1) if classes_m else ""
        
        style_m = re.search(r'style="([^"]+)"', card_content)
        style = style_m.group(1) if style_m else ""
        
        cta_m = re.search(r'href="([^"]+)"[^>]*class="[^"]*service-cta[^"]*"', card_content)
        cta = cta_m.group(1) if cta_m else "None"
        
        print(f"Card {idx+1:2d}: '{title}'\n  Classes: {classes}\n  Style: {style}\n  CTA: {cta}")
        print("-" * 50)
