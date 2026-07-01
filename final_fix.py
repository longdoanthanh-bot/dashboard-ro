import re

# Read index.html
with open('index.html', 'r', encoding='utf-8-sig') as f:
    c = f.read()

# Read tasks.html
with open('tasks.html', 'r', encoding='utf-8-sig') as f:
    t = f.read()

# 1. EXTRACT STOREMAP CONTROLS from panel-storemap
storemap_start = c.find('<div class="map-controls">')
storemap_end = c.find('<div id="nearby-panel"', storemap_start)
storemap_html = c[storemap_start:storemap_end].strip()

# Remove them from panel-storemap
c = c[:storemap_start] + c[storemap_end:]

# 2. EXTRACT TASKS CONTROLS from tasks.html
# We want to extract .stats-row and .add-form
stats_start = t.find('<div class="stats-row">')
# the stats-row block ends with </div> right before <!-- FILTER TABS -->
stats_end_match = re.search(r'</div>\s*<!-- FILTER TABS -->', t)
stats_html = t[stats_start:stats_end_match.start()].strip()
if stats_html.endswith('</div>\n    </div>'):
    stats_html = stats_html[:-10].strip()

add_start = t.find('<div class="add-form">')
add_end = t.find('<!-- STATS -->')
if add_end == -1:
    add_end = stats_start
add_html = t[add_start:add_end].strip()

# Change flex-direction of stat-right-group in tasks.html CSS
t = t.replace('flex-direction:column;', 'flex-direction:row;')

# Remove them from tasks.html
t = t[:add_start - 25] + t[stats_end_match.start():]

# In tasks.html, replace button onclicks to use correct context?
# Actually, since we're moving add_html and stats_html to index.html, we must rewrite the onclicks inside them!
add_html = add_html.replace('onclick="createTask()"', 'onclick="document.getElementById(\'iframe-tasks\').contentWindow.createTask()"')
add_html = add_html.replace('onclick="exportExcel()"', 'onclick="document.getElementById(\'iframe-tasks\').contentWindow.exportExcel()"')

# 3. BUILD HEADER FILTERS for index.html
# We want to place them BETWEEN header-left and header-right
header_left_end = c.find('</div>\n    <div class="header-right"')
if header_left_end == -1:
    header_left_end = c.find('</div>\r\n    <div class="header-right"')

# Storemap filters
# Let's wrap storemap_html in a container
storemap_header_html = f"""
    <div id="storemap-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: column; align-items: flex-start; justify-content: center; gap: 8px;">
        {storemap_html}
    </div>
"""

# Tasks filters: stats on top, add-form below
tasks_header_html = f"""
    <div id="tasks-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: column; align-items: flex-start; justify-content: center; gap: 8px;">
        {stats_html}
        {add_html}
    </div>
"""

# Insert them into index.html
c = c[:header_left_end + 6] + storemap_header_html + tasks_header_html + c[header_left_end + 6:]

# 4. Update switchMain in index.html to toggle header filters properly
# In 88fd7a3, switchMain doesn't hide/show .header-filters
switch_main_start = c.find('function switchMain(panel, btn) {')
switch_main_end = c.find('}', c.find('if (panel === \'tasks\')', switch_main_start))

# We inject the logic to toggle header filters
toggle_logic = """
    document.querySelectorAll('.header-filters').forEach(el => el.style.display = 'none');
    const headerFilter = document.getElementById(panel + '-header-filters');
    if (headerFilter) {
        headerFilter.style.display = 'flex';
    }
"""
insert_pos = c.find('document.getElementById(\'panel-\' + panel).classList.add(\'active\');', switch_main_start)
insert_pos = c.find('\n', insert_pos) + 1
c = c[:insert_pos] + toggle_logic + c[insert_pos:]

# Wait! What about switchMainBySelect?
switch_select_start = c.find('function switchMainBySelect(val) {')
insert_pos2 = c.find('document.getElementById(\'panel-\' + val).classList.add(\'active\');', switch_select_start)
insert_pos2 = c.find('\n', insert_pos2) + 1
toggle_logic2 = """
    document.querySelectorAll('.header-filters').forEach(el => el.style.display = 'none');
    const headerFilter = document.getElementById(val + '-header-filters');
    if (headerFilter) {
        headerFilter.style.display = 'flex';
    }
"""
c = c[:insert_pos2] + toggle_logic2 + c[insert_pos2:]

# 5. Fix Tonkho export table headers (the mojibake issue that was there in javascript, although 88fd7a3 might not have it)
# We already used utf-8-sig, so it's fine.
# 6. We also need to add `.header-filters` to CSS if not present
if '.header-filters' not in c:
    css_insert = c.find('</style>')
    c = c[:css_insert] + '  .header-filters { display:flex; align-items:center; }\n' + c[css_insert:]

# Add styles for stats-row in index.html (since we moved them from tasks.html)
tasks_styles = """
  /* ===== TASKS STATS & ADD FORM IN HEADER ===== */
  .stats-row { flex:0 0 auto; display:flex; gap:6px; align-items:stretch; }
  .stat-total-card {
      flex:0 0 80px; background:var(--bg3); border:1px solid var(--border); border-radius:8px;
      padding:6px 8px; display:flex; flex-direction:column; align-items:center; justify-content:center;
      position:relative; overflow:hidden; transition:background .4s;
  }
  .stat-total-card .stat-num { font-size:20px; font-weight:900; color:#fff; position:relative; z-index:1; text-shadow:0 1px 3px rgba(0,0,0,0.3); }
  .stat-total-card .stat-label { font-size:7px; color:rgba(255,255,255,0.8); text-transform:uppercase; letter-spacing:.4px; margin-top:1px; position:relative; z-index:1; font-weight:700; }
  .stat-total-card .stat-pct { font-size:8px; color:rgba(255,255,255,0.9); font-weight:700; margin-top:2px; position:relative; z-index:1; }
  .stat-right-group {
      flex:0 0 auto; display:flex; flex-direction:row; gap:3px;
  }
  .stat-card { background:var(--bg3); border:1px solid var(--border); border-radius:6px; padding:2px 12px; display:flex; align-items:center; gap:6px; }
  .stat-card .stat-num { font-size:13px; font-weight:800; min-width:18px; text-align:right; }
  .stat-card .stat-label { font-size:7px; color:var(--text3); text-transform:uppercase; letter-spacing:.4px; white-space:nowrap; }
  .stat-card .stat-pct-detail { font-size:9px; font-weight:700; min-width:28px; text-align:right; }
  .stat-card.s-todo .stat-num, .stat-card.s-todo .stat-pct-detail { color:var(--orange); }
  .stat-card.s-doing .stat-num, .stat-card.s-doing .stat-pct-detail { color:var(--yellow); }
  .stat-card.s-done .stat-num, .stat-card.s-done .stat-pct-detail { color:var(--green); }
  
  .add-form {
      flex:1; background:var(--card); border:1px solid var(--border); border-radius:8px;
      padding:8px 14px; display:flex; align-items:flex-end; gap:10px; flex-wrap:wrap;
  }
  .add-form .form-title { font-size:13px; font-weight:700; color:var(--text); display:flex; align-items:center; gap:6px; margin-bottom:0; white-space:nowrap; }
  .form-group { display:flex; flex-direction:column; gap:3px; }
  .form-group label { font-size:9px; color:var(--text3); text-transform:uppercase; letter-spacing:.5px; font-weight:600; }
  .form-input { background:var(--bg3); border:1px solid var(--border); border-radius:8px; color:var(--text); padding:7px 12px; font-size:12px; font-family:inherit; min-width:180px; }
  .form-input:focus { outline:none; border-color:var(--blue); }
  .form-input::placeholder { color:var(--text3); }
  select.form-input { appearance:none; padding-right:28px; cursor:pointer; background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%236c8cff'/%3E%3C/svg%3E"); background-repeat:no-repeat; background-position:right 10px center; }
  .btn-create { padding:7px 20px; border-radius:8px; border:none; background:var(--blue); color:#fff; font-size:12px; font-weight:700; font-family:inherit; cursor:pointer; transition:all .2s; }
  .btn-create:hover { background:#5a7aee; transform:translateY(-1px); }
"""
css_insert = c.find('</style>'); c = c[:css_insert] + tasks_styles + c[css_insert:]


with open('index.html', 'w', encoding='utf-8-sig') as f:
    f.write(c)

# Add getEl logic to tasks.html because we moved elements to index.html
getEl_logic = """
  // Redirect element lookup to parent document if it exists there
  function getEl(id) {
      if (window.parent && window.parent.document && window.parent.document.getElementById(id)) {
          return window.parent.document.getElementById(id);
      }
      return document.getElementById(id);
  }
"""
t_script = t.find('<script>')
t = t[:t_script+8] + getEl_logic + t[t_script+8:]

# Replace document.getElementById with getEl in tasks.html where relevant
# We only care about stat-total, stat-pct, stat-todo, stat-doing, stat-done, pct-todo, pct-doing, pct-done
for stat_id in ['stat-total', 'stat-pct', 'stat-todo', 'stat-doing', 'stat-done', 'pct-todo', 'pct-doing', 'pct-done', 'new-title', 'new-desc', 'new-deadline', 'new-priority']:
    t = t.replace(f"document.getElementById('{stat_id}')", f"getEl('{stat_id}')")
    t = t.replace(f'document.getElementById("{stat_id}")', f'getEl("{stat_id}")')

with open('tasks.html', 'w', encoding='utf-8-sig') as f:
    f.write(t)

print("Files completely patched with UTF-8 BOM")
