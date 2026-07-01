import re

with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# 1. Protect navMenuContainer from shrinking
index_content = index_content.replace(
    '<div style="position: relative; display: flex; align-items: center; gap: 14px;" id="navMenuContainer">',
    '<div style="position: relative; display: flex; align-items: center; gap: 14px; flex-shrink: 0;" id="navMenuContainer">'
)

# 2. Refactor thuhoi-header-filters
index_content = index_content.replace(
    '<div id="thuhoi-header-filters" class="header-filters top-controls-wrapper" style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: flex-end; gap: 8px;">',
    '<div id="thuhoi-header-filters" class="header-filters top-controls-wrapper" style="flex: 1; display: none; flex-direction: row; justify-content: flex-end; align-items: center; gap: 20px;">'
)

# Remove margin-left: auto from trip-date-bar
index_content = index_content.replace(
    '<div class="cal-bar" id="trip-date-bar" style="margin-left: auto; margin-bottom: 0; padding: 0; background: transparent; box-shadow: none;">',
    '<div class="cal-bar" id="trip-date-bar" style="margin-bottom: 0; padding: 0; background: transparent; box-shadow: none;">'
)

thuhoi_filters_block = re.search(
    r'(<div class="filter-row" style="flex-wrap: nowrap; margin-bottom: 0;">.*?<div class="color-legend".*?</div>\s*)</div>\s*<!-- PANEL 3',
    index_content,
    re.DOTALL
)

if thuhoi_filters_block:
    inner = thuhoi_filters_block.group(1)
    new_inner = f'<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 6px;">\n{inner}</div>\n'
    index_content = index_content[:thuhoi_filters_block.start(1)] + new_inner + index_content[thuhoi_filters_block.end(1):]
    
    index_content = index_content.replace(
        '<div class="filter-row" style="flex-wrap: nowrap; margin-bottom: 0;">',
        '<div class="filter-row" style="flex-wrap: nowrap; margin-bottom: 2px;">'
    )


# 3. Move map-controls ONLY to storemap-header-filters
map_controls_match = re.search(
    r'(<div class="map-controls">.*?</div>)\s*<div class="filter-row"',
    index_content,
    re.DOTALL
)

if map_controls_match:
    map_controls_html = map_controls_match.group(1)
    index_content = index_content[:map_controls_match.start(1)] + index_content[map_controls_match.end(1):]
    
    storemap_header_html = f'''<div id="storemap-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: row; align-items: center; justify-content: flex-end;">
{map_controls_html}
</div>
'''
    header_end = index_content.find('</div>\n    </div>\n\n    <div id="navMenuDropdown"')
    if header_end != -1:
        tasks_header_html = '<div id="tasks-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: row; align-items: center; justify-content: flex-end;"></div>\n'
        index_content = index_content[:header_end] + storemap_header_html + tasks_header_html + index_content[header_end:]

# Add basic CSS for add-form in tasks
tasks_css = """
/* ===== TASKS HEADER CSS ===== */
.add-form { display:flex; gap:8px; align-items:flex-end; background:transparent; padding:0; flex:1; max-width: 650px; justify-content: flex-end; }
.form-title { font-size:12px; font-weight:700; color:var(--text); margin-right:4px; margin-bottom: 6px; display:flex; align-items:center; }
.form-group { display:flex; flex-direction:column; gap:4px; }
.form-group label { font-size:9px; color:var(--text3); font-weight:600; text-transform:uppercase; letter-spacing:.5px; }
.form-input { padding:6px 10px; background:var(--bg2); border:1px solid var(--border); border-radius:6px; color:var(--text); font-size:11px; font-family:inherit; outline:none; transition:border-color .2s; }
.form-input:focus { border-color:var(--blue); }
.btn-create { padding:6px 16px; background:var(--blue); color:#fff; border:none; border-radius:6px; font-weight:600; font-size:11px; cursor:pointer; transition:background .2s; height: 28px; }
.btn-create:hover { background:#5a7aee; }
"""

style_end = index_content.find('</style>')
if style_end != -1:
    index_content = index_content[:style_end] + tasks_css + "\n" + index_content[style_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)


# 4. Extract ONLY add-form from tasks.html
with open('tasks.html', 'r', encoding='utf-8') as f:
    tasks_content = f.read()

add_form_match = re.search(r'(<div class="add-form">.*?</div>)\s*<!-- STATS', tasks_content, re.DOTALL)
if add_form_match:
    add_form_html = add_form_match.group(1)
    
    tasks_content = tasks_content[:add_form_match.start(1)] + tasks_content[add_form_match.end(1):]
    tasks_content = tasks_content.replace('<div class="top-row">', '<div class="top-row" style="justify-content: flex-end;">')
    
    helper_script = """
const P_DOC = window.parent.document;
function getEl(id) {
    let el = document.getElementById(id);
    if (!el && P_DOC) el = P_DOC.getElementById(id);
    return el;
}
"""
    tasks_content = tasks_content.replace('<script>', f'<script>\n{helper_script}')
    tasks_content = tasks_content.replace("document.getElementById('new-title')", "getEl('new-title')")
    tasks_content = tasks_content.replace("document.getElementById('new-desc')", "getEl('new-desc')")
    tasks_content = tasks_content.replace("document.getElementById('new-deadline')", "getEl('new-deadline')")
    tasks_content = tasks_content.replace("document.getElementById('new-priority')", "getEl('new-priority')")
    
    with open('tasks.html', 'w', encoding='utf-8') as f:
        f.write(tasks_content)
        
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_content = f.read()
        
    add_form_html = add_form_html.replace('onclick="createTask()"', 'onclick="document.getElementById(\'iframe-tasks\').contentWindow.createTask()"')
    add_form_html = add_form_html.replace('onclick="exportExcel()"', 'onclick="document.getElementById(\'iframe-tasks\').contentWindow.exportExcel()"')

    idx_content = idx_content.replace(
        '<div id="tasks-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: row; align-items: center; justify-content: flex-end;"></div>',
        f'<div id="tasks-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: row; align-items: center; justify-content: flex-end;">\n{add_form_html}\n</div>'
    )
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx_content)

print("Done refactoring UI!")
