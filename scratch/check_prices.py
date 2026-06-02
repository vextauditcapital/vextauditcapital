import subprocess
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

content = subprocess.check_output(['git', 'show', '38daf8f9:index.html'], encoding='utf-8')
prices = re.findall(r'<div class="service-price">(.*?)</div>', content)
print("PRICES IN 38daf8f9:index.html:")
for p in prices:
    print("-", p)
