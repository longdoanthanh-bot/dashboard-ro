import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

match = re.search(r'<div class="top-controls" id="thuhoi-controls".*?<!-- STATS MOVED TO LEFT -->.*?</div>\s*</div>\s*</div>', html, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("Not found")
