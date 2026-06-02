import re

with open('onboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find all divs with class containing 'stp' and print their header/id
steps = re.findall(r'(<div[^>]*class=["\'][^"\']*stp[^"\']*["\'][^>]*>.*?)(?:<div[^>]*class=["\'][^"\']*stp[^"\']*["\']|</div>\s*</div>\s*</body>)', content, re.DOTALL)
print(f"Found {len(steps)} steps in onboard.html")

for i, step in enumerate(re.finditer(r'<div[^>]*class=["\'][^"\']*stp[^"\']*["\'][^>]*>', content)):
    start = step.start()
    # print about 200 chars after start
    print(f"\nStep {i+1} at char {start}:")
    print(content[start:start+400])
