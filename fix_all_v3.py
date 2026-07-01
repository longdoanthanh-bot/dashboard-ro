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
    panel_storemap_start = idx.find('<div class="main-panel" id="panel-storemap">')
    
    filter_row_start = idx.find('<div class="filter-row" style="margin-bottom:4px;">', panel_storemap_start)
    filter_row_end = idx.find('<div class="map-legend">', filter_row_start)
    filter_row_html = idx[filter_row_start:filter_row_end]
    
    map_legend_start = filter_row_end
    map_legend_end = idx.find('<div id="nearby-panel"', map_legend_start)
    map_legend_html = idx[map_legend_start:map_legend_end]

    idx = idx[:filter_row_start] + idx[map_legend_end:]
    filter_row_html = filter_row_html.replace('margin-bottom:4px;', '')

    storemap_header_start = idx.find('<div id="storemap-header-filters" class="header-filters"')
    tasks_header_start = idx.find('<div id="tasks-header-filters"', storemap_header_start)
    
    # Update styling
    old_storemap_style = 'style="flex: 1; display: none; flex-direction: row; align-items: center; justify-content: flex-end;"'
    new_storemap_style = 'style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: flex-end; gap: 4px;"'
    idx = idx.replace(old_storemap_style, new_storemap_style)
    
    old_map_controls = '<div class="map-controls">'
    new_map_controls = '<div class="map-controls" style="display:flex; flex-direction:row; gap:12px; flex-wrap:nowrap; overflow-x:auto;">'
    idx = idx.replace(old_map_controls, new_map_controls)
    
    # We must recalculate tasks_header_start because we just changed string lengths with replace()
    storemap_header_start = idx.find('<div id="storemap-header-filters" class="header-filters"')
    tasks_header_start = idx.find('<div id="tasks-header-filters"', storemap_header_start)
    
    # The storemap-header-filters ends right before tasks-header-filters
    # In fb12a2d:
    # </div>
    # <div id="tasks-header-filters" ...>
    # So the last </div> before tasks_header_start is the closing div of storemap-header-filters.
    last_div_idx = idx.rfind('</div>', storemap_header_start, tasks_header_start)
    # Insert filter_row_html and map_legend_html before this </div>
    idx = idx[:last_div_idx] + filter_row_html + map_legend_html + '\n    ' + idx[last_div_idx:]

    # --- 3. Fix Tasks Layout ---
    stats_row_start = tsk.find('<div class="stats-row">')
    filter_tabs_start = tsk.find('<div class="filter-tabs">', stats_row_start)
    stats_row_html = tsk[stats_row_start:filter_tabs_start].strip()
    
    tsk = tsk[:stats_row_start] + tsk[filter_tabs_start:]

    tasks_header_start = idx.find('<div id="tasks-header-filters"')
    add_form_start = idx.find('<div class="add-form">', tasks_header_start)
    idx = idx[:add_form_start] + stats_row_html + '\n        ' + idx[add_form_start:]
    
    # Replace tasks style
    # Make sure we only replace the one for tasks!
    tasks_header_end = idx.find('>', tasks_header_start)
    tasks_header_tag = idx[tasks_header_start:tasks_header_end+1]
    new_tasks_header_tag = tasks_header_tag.replace(
        'style="flex: 1; display: none; flex-direction: row; align-items: center; justify-content: flex-end;"',
        'style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: flex-end; gap: 8px;"'
    )
    idx = idx[:tasks_header_start] + new_tasks_header_tag + idx[tasks_header_end+1:]
    
    # Extract form css and stats css
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

    # Add form css properly
    with open('tasks.html', 'r', encoding='utf-8') as f:
        tc = f.read()
    start_form_css = tc.find('/* ===== ADD TASK FORM ===== */')
    end_form_css = tc.find('.checklist-item-delete:hover', start_form_css)
    form_css = tc[start_form_css:end_form_css].strip()
    form_css = form_css.replace('flex-wrap:wrap;', 'flex-wrap:nowrap; overflow-x:auto; background:transparent; border:none; padding:0;')
    form_css = form_css.replace('gap:10px;', 'gap:12px;')

    idx_style_end = idx.find('</style>')
    idx = idx[:idx_style_end] + stats_css + '\n' + form_css + '\n' + idx[idx_style_end:]

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
print("Done v3!")
