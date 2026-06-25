with open('onboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for service card containers in onboard.html
# e.g., elements with class="sc" or "service-card"
import re
cards = re.findall(r'<div[^>]*class=["\'][^"\']*sc[^"\']*["\'][^>]*>', content)
print(f"Found {len(cards)} elements with class containing 'sc' in onboard.html:")
for card in cards[:10]:
    print(card)

# Let's search for any occurrence of 'rzp.io' in onboard.html besides the javascript
# or in the card attributes
all_rzp_links = re.findall(r'https?://rzp\.io/rzp/[A-Za-z0-9]+', content)
print(f"\nAll Razorpay links in onboard.html: {len(all_rzp_links)}")
for link in set(all_rzp_links):
    print(f"  {link}")
