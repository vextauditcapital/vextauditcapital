with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's count how many service-cards are there in index.html
import re
cards_raw = re.findall(r'<div class="service-card[^"]*">', content)
print(f"Number of service-card divs: {len(cards_raw)}")

# Print all of them with some surrounding lines
lines = content.splitlines()
for i, line in enumerate(lines):
    if "service-card" in line:
        # Find the title within the next few lines
        title = "UNKNOWN"
        for j in range(i, min(len(lines), i+10)):
            m = re.search(r'<h3 class="service-title">(.*?)</h3>', lines[j])
            if m:
                title = m.group(1)
                break
        print(f"Line {i+1}: {line.strip()} | Title: {title}")
