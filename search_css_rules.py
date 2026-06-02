import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's extract the <style> content
style_m = re.search(r'<style>(.*?)</style>', text, re.DOTALL)
if style_m:
    style_content = style_m.group(1)
    
    # Search for services-grid or service-card styling, or display properties
    print("CSS lines containing display: none or similar:")
    for line in style_content.splitlines():
        if "display:" in line or "visibility:" in line or "opacity:" in line or "height: 0" in line:
            print(" ", line.strip())
            
    # Search for specific grid styles
    print("\nGrid/Card specific styles:")
    for line in style_content.splitlines():
        if "services-grid" in line or "service-card" in line:
            print(" ", line.strip())
else:
    print("No inline style tag found!")
