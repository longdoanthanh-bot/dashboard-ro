import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Thu hoi alignment
# Current: <div id="thuhoi-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: column; align-items: flex-end;">
content = content.replace(
    '<div id="thuhoi-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: column; align-items: flex-end;">',
    '<div id="thuhoi-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: row; justify-content: space-between; align-items: flex-end;">'
)

# We need to wrap `filter-row` and `color-legend` inside a div so they stack properly on the right.
thuhoi_filters_block = re.search(
    r'(<div class="filter-row" style="flex-wrap: nowrap; margin-bottom: 0;">.*?<div class="color-legend".*?</div>\s*)</div>\s*<!-- PANEL 3: SO D\? ST -->',
    content,
    re.DOTALL
)

if thuhoi_filters_block:
    inner = thuhoi_filters_block.group(1)
    new_inner = f'<div style="display: flex; flex-direction: column; align-items: flex-end;">\n{inner}</div>\n'
    content = content[:thuhoi_filters_block.start(1)] + new_inner + content[thuhoi_filters_block.end(1):]
else:
    print("Could not find thuhoi_filters_block!")

# Let's verify `trip-date-bar` margin
content = content.replace(
    '<div class="trip-date-bar" style="margin-bottom: 5px;">',
    '<div class="trip-date-bar" style="margin-bottom: 0;">'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated thuhoi successfully")
