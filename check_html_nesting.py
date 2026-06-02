import re

with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Let's count unclosed <div> tags and trace their levels
depth = 0
card_lines = []
for i, line in enumerate(lines):
    # Strip comments to avoid false matches
    clean_line = re.sub(r"<!--.*?-->", "", line)
    
    # Check for opening divs
    div_opens = len(re.findall(r"<div\b", clean_line))
    div_closes = len(re.findall(r"</div\b", clean_line))
    
    prev_depth = depth
    depth += div_opens - div_closes
    
    if "service-card" in line:
        # Find title
        title = "UNKNOWN"
        for j in range(i, min(len(lines), i+15)):
            m = re.search(r'<h3 class="service-title">(.*?)</h3>', lines[j])
            if m:
                title = m.group(1).strip()
                break
        card_lines.append((i+1, title, prev_depth, depth))

print(f"Total lines: {len(lines)}")
print(f"Final depth at end of file: {depth}")
print("\nService card depths and positions:")
for idx, (line_no, title, d_before, d_after) in enumerate(card_lines):
    print(f"Card {idx+1:2d} (Line {line_no:4d}): '{title}' | Depth Before: {d_before} | Depth After: {d_after}")
