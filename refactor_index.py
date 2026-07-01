import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Thu hoi header filters alignment
# Change the container flex properties
content = content.replace(
    '<div id="thuhoi-header-filters" class="header-filters top-controls-wrapper" style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: flex-end; gap: 8px;">',
    '<div id="thuhoi-header-filters" class="header-filters top-controls-wrapper" style="flex: 1; display: none; flex-direction: row; justify-content: space-between; align-items: flex-end; gap: 16px;">'
)

# Extract filter-row and color-legend, wrap them in a flex-col div so they stack on the right
thuhoi_filters_block = re.search(
    r'(<div class="filter-row" style="flex-wrap: nowrap; margin-bottom: 0;">.*?<div class="color-legend".*?</div>\s*)</div>\s*</header>',
    content,
    re.DOTALL
)

if thuhoi_filters_block:
    inner = thuhoi_filters_block.group(1)
    # Wrap in flex-col
    new_inner = f'<div style="display: flex; flex-direction: column; align-items: flex-end; gap: 6px;">\n{inner}</div>\n'
    content = content[:thuhoi_filters_block.start(1)] + new_inner + content[thuhoi_filters_block.end(1):]
    
    # Update margin-bottom of filter-row inside new_inner so they stack nicely with color-legend
    content = content.replace(
        '<div class="filter-row" style="flex-wrap: nowrap; margin-bottom: 0;">',
        '<div class="filter-row" style="flex-wrap: nowrap; margin-bottom: 4px;">'
    )
else:
    print("Could not find thuhoi filter block!")


# 2. Extract map controls and insert into header
map_controls_match = re.search(
    r'(<div class="map-controls">.*?<div class="map-legend">.*?</div>)',
    content,
    re.DOTALL
)

if map_controls_match:
    map_controls_html = map_controls_match.group(1)
    
    # Remove from panel-storemap
    content = content[:map_controls_match.start(1)] + content[map_controls_match.end(1):]
    
    # Wrap in storemap-header-filters
    storemap_header_html = f'''<div id="storemap-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: flex-end; gap: 8px;">
{map_controls_html}
</div>
'''
    # We will inject it before </header>
    header_end = content.find('</header>')
    if header_end != -1:
        # Also prepare tasks-header-filters
        tasks_header_html = '<div id="tasks-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: flex-end; gap: 8px;"></div>\n'
        
        content = content[:header_end] + storemap_header_html + tasks_header_html + content[header_end:]
    else:
        print("Could not find header injection point!")
else:
    print("Could not find map controls!")


# 3. Add CSS for tasks to index.html
tasks_css = """
/* ===== TASKS HEADER CSS ===== */
.top-row { display:flex; gap:10px; margin-bottom:6px; align-items:stretch; width: 100%; justify-content: flex-end; }
.add-form { display:flex; gap:8px; align-items:flex-end; background:var(--bg3); padding:8px 12px; border-radius:8px; border:1px solid var(--border); flex:1; max-width: 800px;}
.form-title { font-size:12px; font-weight:700; color:var(--text); margin-right:4px; margin-bottom: 6px; display:flex; align-items:center; }
.form-group { display:flex; flex-direction:column; gap:4px; }
.form-group label { font-size:9px; color:var(--text3); font-weight:600; text-transform:uppercase; letter-spacing:.5px; }
.form-input { padding:6px 10px; background:var(--bg2); border:1px solid var(--border); border-radius:6px; color:var(--text); font-size:11px; font-family:inherit; outline:none; transition:border-color .2s; }
.form-input:focus { border-color:var(--blue); }
.btn-create { padding:6px 16px; background:var(--blue); color:#fff; border:none; border-radius:6px; font-weight:600; font-size:11px; cursor:pointer; transition:background .2s; height: 28px; }
.btn-create:hover { background:#5a7aee; }
.stats-row { display:flex; gap:8px; }
.stat-total-card { background:#34d399; color:#000; padding:8px 12px; border-radius:8px; display:flex; flex-direction:column; align-items:center; justify-content:center; min-width:60px; font-weight:800; }
.stat-total-card .stat-num { font-size:18px; line-height:1; }
.stat-total-card .stat-label { font-size:9px; text-transform:uppercase; opacity:.8; margin-top:2px; }
.stat-total-card .stat-pct { font-size:10px; margin-top:2px; }
.stat-right-group { display:flex; flex-direction:column; gap:4px; }
.stat-card { display:flex; align-items:center; justify-content:space-between; background:var(--bg3); border:1px solid var(--border); border-radius:4px; padding:2px 8px; font-size:10px; width:120px; }
.stat-card .stat-num { font-weight:700; width:16px; }
.stat-card .stat-label { color:var(--text2); flex:1; }
.stat-card .stat-pct-detail { font-weight:700; width:24px; text-align:right; }
.stat-card.s-todo { border-left:3px solid var(--orange); }
.stat-card.s-todo .stat-num { color:var(--orange); }
.stat-card.s-doing { border-left:3px solid var(--yellow); }
.stat-card.s-doing .stat-num { color:var(--yellow); }
.stat-card.s-done { border-left:3px solid var(--green); }
.stat-card.s-done .stat-num { color:var(--green); }

.filter-tabs { display:flex; gap:6px; align-items:center; }
.filter-tab { padding:4px 12px; border-radius:20px; border:1px solid var(--border); background:var(--bg3); color:var(--text2); font-size:11px; font-weight:600; cursor:pointer; transition:all .2s; }
.filter-tab:hover { border-color:var(--blue); color:var(--text); }
.filter-tab.active { background:var(--blue); border-color:var(--blue); color:#fff; }
"""

# Inject CSS
style_end = content.find('</style>')
if style_end != -1:
    content = content[:style_end] + tasks_css + "\n" + content[style_end:]
else:
    print("Could not find style tag!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html successfully")
