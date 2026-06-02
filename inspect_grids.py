import re
import sys

# Ensure UTF-8 output for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's find all '<div class="services-grid">' or other grids
grids = list(re.finditer(r'<div class="services-grid[^"]*">', text))
print(f"Total services-grids: {len(grids)}")

for idx, grid_match in enumerate(grids):
    start_pos = grid_match.start()
    next_pos = len(text)
    if idx + 1 < len(grids):
        next_pos = grids[idx+1].start()
    
    # Check for another section
    next_sec = list(re.finditer(r'<section\b|<footer\b', text[start_pos:next_pos]))
    if next_sec:
        next_pos = start_pos + next_sec[0].start()
    
    grid_content = text[start_pos:next_pos]
    # Count how many service-cards are in this grid content
    cards_in_grid = re.findall(r'<div class="service-card[^"]*"', grid_content)
    
    preceding = text[max(0, start_pos-200):start_pos]
    label_match = re.search(r'<span class="services-section-label[^"]*">(.*?)</span>', preceding)
    label = label_match.group(1).strip() if label_match else "No label found"
    
    print(f"Grid {idx+1}: label='{label}' | cards in grid={len(cards_in_grid)}")
    snippet = text[start_pos:start_pos+150].strip()
    # Replace non-ascii chars just in case
    clean_snippet = "".join([c if ord(c) < 128 else f"\\u{ord(c):04x}" for c in snippet])
    print(f"  Snippet of start: {clean_snippet}")
    print("-" * 50)
