import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Expand container width
content = content.replace('max-width:1400px;', 'max-width:98%;')

# 2. Fix CSS for top-controls-wrapper
old_css = '.top-controls-wrapper { position:fixed; top:12px; left:410px; z-index:1005; display:flex; flex-direction:column; gap:4px; }'
new_css = '.top-controls-wrapper { display:flex; flex-direction:column; gap:4px; margin-left:20px; }'
content = content.replace(old_css, new_css)

# 3. Extract top-controls-wrapper HTML
extract_pattern = re.compile(r'(<div class="top-controls-wrapper">.*?</select>\s*</div>\s*</div>\s*</div>\s*<div class="filter-group">.*?</div>\s*</div>\s*<div class="color-legend">.*?</div>\s*</div>)', re.DOTALL)
match = extract_pattern.search(content)

if match:
    wrapper_html = match.group(1)
    # Add id and class
    wrapper_html_mod = wrapper_html.replace('<div class="top-controls-wrapper">', '<div id="tonkho-header-filters" class="header-filters top-controls-wrapper" style="flex: 1;">')

    # Remove from original location
    content = content.replace(wrapper_html, '')

    # 4. Insert into header
    header_insert_point = r'(</h1>\s*<div id="navMenuDropdown".*?</div>\s*</div>)'
    content = re.sub(header_insert_point, r'\1\n    ' + wrapper_html_mod.replace('\\', '\\\\'), content)
else:
    print("WARNING: Could not extract wrapper. Check regex.")

# 5. Update switchMain
old_switch_main = "document.getElementById('panel-' + panel).classList.add('active');"
new_switch_main = "document.getElementById('panel-' + panel).classList.add('active');\n    document.querySelectorAll('.header-filters').forEach(el => el.style.display = 'none');\n    if (document.getElementById(panel + '-header-filters')) document.getElementById(panel + '-header-filters').style.display = 'flex';"
content = content.replace(old_switch_main, new_switch_main)

# Also update switchMainBySelect just in case
old_switch_main_sel = "document.getElementById('panel-' + val).classList.add('active');"
new_switch_main_sel = "document.getElementById('panel-' + val).classList.add('active');\n    document.querySelectorAll('.header-filters').forEach(el => el.style.display = 'none');\n    if (document.getElementById(val + '-header-filters')) document.getElementById(val + '-header-filters').style.display = 'flex';"
content = content.replace(old_switch_main_sel, new_switch_main_sel)

# Initialize display on load
init_display = "document.querySelectorAll('.header-filters').forEach(el => el.style.display = 'none');\nif (document.getElementById('tonkho-header-filters')) document.getElementById('tonkho-header-filters').style.display = 'flex';"
if 'header-filters' not in content[:content.find('</head>')]:
    # just put it near the end of body
    content = content.replace('</body>', f'<script>{init_display}</script>\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated successfully")
