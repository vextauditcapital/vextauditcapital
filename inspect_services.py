import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Find all headings/sections and the number of cards under them
sections = re.split(r'(<section[^>]* id="[^"]+"[^>]*>)', text)
print(f"Total sections: {len(sections)}")

for i, part in enumerate(sections):
    if part.startswith("<section"):
        id_match = re.search(r'id="([^"]+)"', part)
        sec_id = id_match.group(1) if id_match else "unknown"
        
        # Check the content of this section up to the next section
        content = sections[i+1] if i+1 < len(sections) else ""
        
        # Count service-cards inside this section
        card_titles = re.findall(r'<h3 class="service-title">([^<]+)</h3>', content)
        print(f"Section ID: '{sec_id}' | Cards count: {len(card_titles)}")
        for idx, title in enumerate(card_titles):
            # Let's find the link / CTA
            # Find the card block containing this title
            # Let's get the text around the title
            title_pos = content.find(title)
            surrounding = content[max(0, title_pos-300):min(len(content), title_pos+500)]
            cta_match = re.search(r'href="([^"]+)"[^>]*class="[^"]*service-cta[^"]*"', surrounding)
            cta = cta_match.group(1) if cta_match else "No CTA found"
            
            # check if there's display: none or inline style on the card itself
            card_match = re.search(r'<div class="service-card[^"]*"[^>]*style="([^"]+)"', surrounding)
            style = card_match.group(1) if card_match else ""
            
            print(f"  {idx+1}. Title: '{title.strip()}' | CTA Link: '{cta}' | Style: '{style}'")
