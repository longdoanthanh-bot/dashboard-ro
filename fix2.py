import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'gap: 8px;\s*<div class="filter-row"', 'gap: 8px;">\n    <div class="filter-row"', c)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
