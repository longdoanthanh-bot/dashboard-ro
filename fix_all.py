import re

def fix():
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()
    with open('tasks.html', 'r', encoding='utf-8') as f:
        tsk = f.read()

    # --- 1. Fix TonKho Layout ---
    old_tonkho = '<div id="tonkho-header-filters" class="header-filters top-controls-wrapper" style="flex: 1; display: none;">'
    new_tonkho = '<div id="tonkho-header-filters" class="header-filters top-controls-wrapper" style="flex: 1; display: none; align-items: flex-end;">'
    idx = idx.replace(old_tonkho, new_tonkho)

    # --- 2. Fix Storemap Layout ---
    # Extract filter-row and map-legend from panel-storemap
    panel_storemap_start = idx.find('<div class="main-panel" id="panel-storemap">')
    
    # filter_row starts with <div class="filter-row" style="margin-bottom:4px;">
    filter_row_start = idx.find('<div class="filter-row" style="margin-bottom:4px;">', panel_storemap_start)
    filter_row_end = idx.find('<div class="map-legend">', filter_row_start)
    filter_row_html = idx[filter_row_start:filter_row_end]
    
    map_legend_start = filter_row_end
    map_legend_end = idx.find('<div id="nearby-panel"', map_legend_start)
    map_legend_html = idx[map_legend_start:map_legend_end]

    # Remove them from panel-storemap
    idx = idx[:filter_row_start] + idx[map_legend_end:]

    # Make filter_row and map_legend horizontal
    # filter_row_html is already horizontal. We might want to remove margin-bottom.
    filter_row_html = filter_row_html.replace('margin-bottom:4px;', '')
    # map_legend_html is already horizontal.

    # Insert into storemap-header-filters
    storemap_header_start = idx.find('<div id="storemap-header-filters" class="header-filters"')
    storemap_header_end = idx.find('</header>', storemap_header_start)
    
    # Change style of storemap-header-filters to flex column
    # Current: style="flex: 1; display: none; flex-direction: row; align-items: center; justify-content: flex-end;"
    old_storemap_style = 'style="flex: 1; display: none; flex-direction: row; align-items: center; justify-content: flex-end;"'
    new_storemap_style = 'style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: flex-end; gap: 4px;"'
    idx = idx.replace(old_storemap_style, new_storemap_style)
    
    # Find the end of map-controls inside storemap-header-filters
    map_controls_start = idx.find('<div class="map-controls">', storemap_header_start)
    map_controls_end = idx.find('</div>\n    <div id="tasks-header-filters"', map_controls_start)
    
    # Insert filter_row and map_legend inside map-controls?
    # Actually, they are siblings to map-controls in the new layout, or children.
    # We will make map-controls flex-wrap: nowrap.
    # Current map-controls: <div class="map-controls">
    old_map_controls = '<div class="map-controls">'
    new_map_controls = '<div class="map-controls" style="display:flex; flex-direction:row; gap:12px; flex-wrap:nowrap; overflow-x:auto;">'
    idx = idx.replace(old_map_controls, new_map_controls)
    
    # Insert after map-controls
    # We need to find the closing </div> of map-controls. In fb12a2d, map-controls ends right before the closing </div> of storemap-header-filters.
    # Wait, storemap-header-filters has 2 divs? No, let's just use string replacement on the end tag of map-controls inside header.
    # Let's find exactly the end of storemap-header-filters.
    sm_hf_block = idx[storemap_header_start:storemap_header_end]
    # Replace the last </div> of this block with </div> + filter_row_html + map_legend_html
    last_div_idx = sm_hf_block.rfind('</div>')
    new_sm_hf_block = sm_hf_block[:last_div_idx] + '</div>\n' + filter_row_html + map_legend_html
    idx = idx.replace(sm_hf_block, new_sm_hf_block)

    # --- 3. Fix Tasks Layout ---
    # tasks-header-filters already contains add-form in fb12a2d.
    # We need to add stats-row.
    stats_row_start = tsk.find('<div class="stats-row">')
    stats_row_end = tsk.find('<!-- KANBAN BOARD -->', stats_row_start)
    stats_row_html = tsk[stats_row_start:stats_row_end].strip()
    
    # Remove stats-row from tasks.html
    tsk = tsk[:stats_row_start] + tsk[stats_row_end:]

    # Insert stats-row into tasks-header-filters, ABOVE add-form
    tasks_header_start = idx.find('<div id="tasks-header-filters"')
    add_form_start = idx.find('<div class="add-form">', tasks_header_start)
    idx = idx[:add_form_start] + stats_row_html + '\n        ' + idx[add_form_start:]
    
    # Update tasks-header-filters style to column
    old_tasks_style = 'style="flex: 1; display: none; flex-direction: row; align-items: center; justify-content: flex-end;"'
    new_tasks_style = 'style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: flex-end; gap: 8px;"'
    idx = idx.replace(old_tasks_style, new_tasks_style)
    
    # Also we must copy the CSS for stats-row from tasks.html to index.html
    stats_css = """.stats-row { flex:0 0 auto; display:flex; gap:6px; align-items:stretch; }
.stat-total-card {
    flex:0 0 80px; background:var(--bg3); border:1px solid var(--border); border-radius:8px;
    padding:6px 8px; display:flex; flex-direction:column; align-items:center; justify-content:center;
    position:relative; overflow:hidden; transition:background .4s;
}
.stat-total-card .stat-num { font-size:20px; font-weight:900; color:#fff; position:relative; z-index:1; text-shadow:0 1px 3px rgba(0,0,0,0.3); }
.stat-total-card .stat-label { font-size:7px; color:rgba(255,255,255,0.8); text-transform:uppercase; letter-spacing:.4px; margin-top:1px; position:relative; z-index:1; font-weight:700; }
.stat-total-card .stat-pct { font-size:8px; color:rgba(255,255,255,0.9); font-weight:700; margin-top:2px; position:relative; z-index:1; }
.stat-right-group {
    flex:0 0 auto; display:flex; flex-direction:column; gap:3px;
}
.stat-card { background:var(--bg3); border:1px solid var(--border); border-radius:6px; padding:2px 12px; display:flex; align-items:center; gap:6px; }
.stat-card .stat-num { font-size:13px; font-weight:800; min-width:18px; text-align:right; }
.stat-card .stat-label { font-size:8px; color:var(--text3); text-transform:uppercase; flex:1; font-weight:600; }
.stat-card .stat-pct-detail { font-size:9px; color:var(--text); font-weight:700; text-align:right; min-width:24px; }
.s-todo .stat-num { color:var(--red); }
.s-doing .stat-num { color:var(--yellow); }
.s-done .stat-num { color:var(--green); }"""
    
    idx_style_end = idx.find('</style>')
    idx = idx[:idx_style_end] + stats_css + '\n' + idx[idx_style_end:]

    # Update tasks.html JS to use getEl for stats
    tsk = tsk.replace("document.getElementById('stat-total')", "getEl('stat-total')")
    tsk = tsk.replace("document.getElementById('stat-todo')", "getEl('stat-todo')")
    tsk = tsk.replace("document.getElementById('stat-doing')", "getEl('stat-doing')")
    tsk = tsk.replace("document.getElementById('stat-done')", "getEl('stat-done')")
    tsk = tsk.replace("document.getElementById('stat-pct')", "getEl('stat-pct')")
    tsk = tsk.replace("document.getElementById('pct-todo')", "getEl('pct-todo')")
    tsk = tsk.replace("document.getElementById('pct-doing')", "getEl('pct-doing')")
    tsk = tsk.replace("document.getElementById('pct-done')", "getEl('pct-done')")
    tsk = tsk.replace("document.getElementById('stat-total-card')", "getEl('stat-total-card')")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx)
    with open('tasks.html', 'w', encoding='utf-8') as f:
        f.write(tsk)

fix()
print("Done!")
