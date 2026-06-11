import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Accessibility: Heading Hierarchy
# VextIntel section uses h4 directly after h2. Convert h4 to h3.
content = content.replace('<h4>Monthly Regulatory Digest</h4>', '<h3>Monthly Regulatory Digest</h3>')
content = content.replace('<h4>Real-Time Risk Alerts</h4>', '<h3>Real-Time Risk Alerts</h3>')
content = content.replace('<h4>Dedicated Compliance Advisor</h4>', '<h3>Dedicated Compliance Advisor</h3>')
content = content.replace('<h4>Compliance Calendar</h4>', '<h3>Compliance Calendar</h3>')
content = content.replace('<h4>Quarterly Health Check</h4>', '<h3>Quarterly Health Check</h3>')
content = content.replace('<h4>Priority Audit Access</h4>', '<h3>Priority Audit Access</h3>')

# Footer section uses h4 directly.
content = content.replace('<h4>India Core</h4>', '<h3>India Core</h3>')
content = content.replace('<h4>India Statutory</h4>', '<h3>India Statutory</h3>')
content = content.replace('<h4>Global</h4>', '<h3>Global</h3>')

# Fix CSS for the above changes
content = content.replace('.vi-feature h4{', '.vi-feature h3{')
content = content.replace('.footer-col h4{', '.footer-col h3{')

# 2. Accessibility: Contrast Ratio
# Bump opacity up for all text elements that might fail contrast
content = re.sub(r'opacity:\s*0\.[2-6][0-9]?;', 'opacity: 0.85;', content)

# 3. Performance: Render-Blocking Resources (Fonts)
font_link = '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet"/>'
optimized_font_link = '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="preload" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap\"></noscript>'
content = content.replace(font_link, optimized_font_link)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("index.html optimized successfully.")
