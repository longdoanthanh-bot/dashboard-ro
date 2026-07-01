import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix tonkho header alignment
old_tonkho = '<div id="tonkho-header-filters" class="header-filters top-controls-wrapper" style="flex: 1; display: flex;">'
new_tonkho = '<div id="tonkho-header-filters" class="header-filters top-controls-wrapper" style="flex: 1; display: flex; align-items: flex-end;">'

c = c.replace(old_tonkho, new_tonkho)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed tonkho")
