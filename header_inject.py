import re

# Read files (which are currently clean UTF-8 from git reset)
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
with open('tasks.html', 'r', encoding='utf-8') as f:
    t = f.read()

# 1. Storemap controls
sm_start = c.find('<div class="map-controls">')
sm_end = c.find('<div id="nearby-panel"', sm_start)
sm_html = c[sm_start:sm_end].strip()
c = c[:sm_start] + c[sm_end:] # remove from body

# 2. Tasks controls
t_stats_s = t.find('<div class="stats-row">')
t_stats_e_match = re.search(r'</div>\s*<!-- FILTER TABS -->', t)
t_stats = t[t_stats_s:t_stats_e_match.start()].strip()
if t_stats.endswith('</div>\n    </div>'):
    t_stats = t_stats[:-10].strip()

t_add_s = t.find('<div class="add-form">')
t_add_e = t.find('<!-- STATS -->')
if t_add_e == -1:
    t_add_e = t_stats_s
t_add = t[t_add_s:t_add_e].strip()

# Make stat-right-group row
t = t.replace('flex-direction:column;', 'flex-direction:row;')
t_stats = t_stats.replace('flex-direction:column;', 'flex-direction:row;')

# Remove from tasks.html
t = t[:t_add_s - 25] + t[t_stats_e_match.start():]

# Redirect iframe calls in add form
t_add = t_add.replace('onclick="createTask()"', 'onclick="document.getElementById(\'iframe-tasks\').contentWindow.createTask()"')
t_add = t_add.replace('onclick="exportExcel()"', 'onclick="document.getElementById(\'iframe-tasks\').contentWindow.exportExcel()"')

# 3. Create header wrappers
sm_wrapper = f"""
    <div id="storemap-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: column; align-items: flex-start; justify-content: center; gap: 8px;">
        {sm_html}
    </div>
"""

tasks_wrapper = f"""
    <div id="tasks-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: column; align-items: flex-start; justify-content: center; gap: 8px;">
        {t_stats}
        {t_add}
    </div>
"""

# 4. Inject into header in index.html
# Find where tonkho-header-filters ends
tonkho_start = c.find('<div id="tonkho-header-filters"')
# Find the end of tonkho-header-filters which is right before header-right
header_right = c.find('<div class="header-right"')
inject_pos = header_right

c = c[:inject_pos] + sm_wrapper + tasks_wrapper + c[inject_pos:]

# 5. Inject CSS for tasks into index.html
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
css_insert = c.find('</style>')
c = c[:css_insert] + tasks_styles + c[css_insert:]

# 6. Inject JS toggle logic in index.html
switch_main_start = c.find('function switchMain(panel, btn) {')
insert_pos = c.find('document.getElementById(\'panel-\' + panel).classList.add(\'active\');', switch_main_start)
insert_pos = c.find('\n', insert_pos) + 1
toggle_logic = """
    document.querySelectorAll('.header-filters').forEach(el => el.style.display = 'none');
    const headerFilter = document.getElementById(panel + '-header-filters');
    if (headerFilter) {
        headerFilter.style.display = 'flex';
    }
"""
c = c[:insert_pos] + toggle_logic + c[insert_pos:]

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

# 7. Add getEl logic to tasks.html
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

for stat_id in ['stat-total', 'stat-pct', 'stat-todo', 'stat-doing', 'stat-done', 'pct-todo', 'pct-doing', 'pct-done', 'new-title', 'new-desc', 'new-deadline', 'new-priority']:
    t = t.replace(f"document.getElementById('{stat_id}')", f"getEl('{stat_id}')")
    t = t.replace(f'document.getElementById("{stat_id}")', f'getEl("{stat_id}")')

# Write back with BOM
with open('index.html', 'w', encoding='utf-8-sig') as f:
    f.write(c)
with open('tasks.html', 'w', encoding='utf-8-sig') as f:
    f.write(t)

print("SUCCESS")
