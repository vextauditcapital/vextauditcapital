import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all blocks of service cards in index.html
# Typically <div class="service-card" ...> or similar
cards = re.findall(r'<div class="[^"]*card[^"]*"[^>]*>.*?</div>', content, re.IGNORECASE | re.DOTALL)
print(f"Found {len(cards)} elements with class containing 'card'.")

# Let's search for any <a href="..."> elements inside the services section
# Let's find all hrefs in the services section
services_sec_match = re.search(r'<section id="services".*?</section>', content, re.DOTALL)
if services_sec_match:
    services_sec = services_sec_match.group(0)
    print("\nInside <section id=\"services\">:")
    hrefs = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', services_sec, re.IGNORECASE | re.DOTALL)
    for idx, (href, text) in enumerate(hrefs, 1):
        text_clean = re.sub(r'<[^>]+>', '', text).strip()
        text_clean = re.sub(r'\s+', ' ', text_clean)
        print(f"  {idx:02d}. Href: '{href}' | Text: '{text_clean[:60]}'")
else:
    print("Could not find <section id=\"services\">.")

# Let's check other sections as well (pricing, vextintel)
pricing_sec_match = re.search(r'<section id="pricing".*?</section>', content, re.DOTALL)
if pricing_sec_match:
    pricing_sec = pricing_sec_match.group(0)
    print("\nInside <section id=\"pricing\">:")
    hrefs = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', pricing_sec, re.IGNORECASE | re.DOTALL)
    for idx, (href, text) in enumerate(hrefs, 1):
        text_clean = re.sub(r'<[^>]+>', '', text).strip()
        text_clean = re.sub(r'\s+', ' ', text_clean)
        print(f"  {idx:02d}. Href: '{href}' | Text: '{text_clean[:60]}'")
