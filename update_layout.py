import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Move header-right to the left
content = re.sub(
    r'(</h1>\s*<div id="navMenuDropdown")',
    r'</h1>\n        \n        <div class="header-right" style="display: flex; align-items: center; gap: 20px; margin-left: 20px;">\n            <button id="themeToggle" onclick="toggleTheme()" style="background: var(--bg2); border: 1px solid var(--border); color: var(--text); padding: 8px 12px; border-radius: var(--radius); cursor: pointer; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 6px; transition: all 0.2s;">\n                <span id="themeIcon">☀️</span> Giao diện\n            </button>\n            <div>Cập nhật: 01/07/2026 14:15</div>\n        </div>\n\n        <div id="navMenuDropdown"',
    content
)

# 2. Remove header-right from the end of header
content = re.sub(
    r'<div class="header-right" style="display: flex; align-items: center; gap: 20px;">\s*<button id="themeToggle"[^>]+>\s*<span id="themeIcon">.*?</span> Giao diện\s*</button>\s*<div>Cập nhật:.*?</div>\s*</div>\s*</header>',
    r'</header>',
    content
)

# 3. Extract trip-date-bar from body
trip_date_bar_match = re.search(r'<div class="cal-bar" id="trip-date-bar".*?</div>\s*</div>\s*</div>', content, re.DOTALL)
trip_date_bar_html = trip_date_bar_match.group(0)

# Remove trip-date-bar and the flex wrapper around basket-summary
content = re.sub(
    r'<div style="display: flex; gap: 20px; align-items: flex-start; justify-content: flex-end; margin-bottom: 10px;">\s*(<div class="basket-summary-panel" id="basket-summary".*?</div>\s*</div>)\s*<div class="cal-bar" id="trip-date-bar".*?</div>\s*</div>\s*</div>\s*</div>',
    r'\1',
    content,
    flags=re.DOTALL
)

# 4. Update thuhoi-header-filters and insert trip-date-bar
new_thuhoi_filters = f'''<div id="thuhoi-header-filters" class="header-filters top-controls-wrapper" style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: flex-end; gap: 8px;">
        {trip_date_bar_html.replace('margin-left: auto; margin-bottom: 0;', 'margin-left: auto; margin-bottom: 0; padding: 0; background: transparent; box-shadow: none;')}
        <div class="filter-row" style="flex-wrap: nowrap; margin-bottom: 0;">'''

content = re.sub(
    r'<div id="thuhoi-header-filters" class="header-filters top-controls-wrapper" style="flex: 1; display: none;">\s*<div class="filter-row">',
    new_thuhoi_filters,
    content
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced successfully")
