import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# --- 1. Fix TAB CÔNG VIỆC (Tasks) ---
# Dàn đều ra (spread horizontally)
# Change .add-form CSS
old_tasks_css = """/* ===== TASKS HEADER CSS ===== */
.add-form { display:flex; gap:8px; align-items:flex-end; background:transparent; padding:0; flex:1; max-width: 650px; justify-content: flex-end; }"""
new_tasks_css = """/* ===== TASKS HEADER CSS ===== */
.add-form { display:flex; gap:12px; align-items:flex-end; background:transparent; padding:0; flex:1; justify-content: flex-end; flex-wrap: nowrap; overflow-x: auto; }
.add-form .form-title { white-space: nowrap; }
.add-form .form-group { white-space: nowrap; }"""
content = content.replace(old_tasks_css, new_tasks_css)


# --- 2. Fix TAB THU HỒI ---
# Current structure:
# <div id="thuhoi-header-filters" ... flex-direction: row; ...>
#    <div id="trip-date-bar"> ... </div>
#    <div flex-col>
#       <div filter-row> ... </div>
#       <div color-legend> ... </div>
#    </div>
# </div>
#
# Target structure:
# <div id="thuhoi-header-filters" style="... flex-direction: column; align-items: flex-end; gap: 8px;">
#    <div filter-row> ... </div>
#    <div style="display: flex; flex-direction: row; align-items: flex-end; gap: 20px;">
#       <div id="trip-date-bar"> ... </div>
#       <div color-legend> ... </div>
#    </div>
# </div>

thuhoi_match = re.search(
    r'<div id="thuhoi-header-filters".*?justify-content: flex-end; align-items: center; gap: 20px;">(.*?)</div>\s*<div id="storemap-header-filters"',
    content,
    re.DOTALL
)

if thuhoi_match:
    thuhoi_inner = thuhoi_match.group(1)
    # extract the parts
    date_bar_match = re.search(r'(<div class="cal-bar" id="trip-date-bar".*?</div>\s*</div>\s*</div>\s*</div>)', thuhoi_inner, re.DOTALL)
    filter_row_match = re.search(r'(<div class="filter-row".*?</div>)\s*<div class="color-legend"', thuhoi_inner, re.DOTALL)
    legend_match = re.search(r'(<div class="color-legend".*?</div>)', thuhoi_inner, re.DOTALL)
    
    if date_bar_match and filter_row_match and legend_match:
        date_bar = date_bar_match.group(1)
        filter_row = filter_row_match.group(1)
        legend = legend_match.group(1)
        
        new_thuhoi_inner = f"""
    {filter_row}
    <div style="display: flex; flex-direction: row; align-items: center; gap: 20px; justify-content: flex-end; width: 100%;">
        {date_bar}
        {legend}
    </div>
"""
        # Replace the wrapper div attributes
        content = re.sub(
            r'<div id="thuhoi-header-filters".*?>',
            '<div id="thuhoi-header-filters" class="header-filters top-controls-wrapper" style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: center; gap: 8px;">',
            content
        )
        # Replace inner HTML
        content = content[:thuhoi_match.start(1)] + new_thuhoi_inner + content[thuhoi_match.end(1):]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done adjusting layout!")
