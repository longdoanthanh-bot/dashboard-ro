"""
Apply all arrow-indicated UI changes:
1. Header: Move "Giao dien + Cap nhat" to LEFT side
2. Tonkho: Move filter row ABOVE stats bar
3. Thu hoi: Move calendar ABOVE chi tiet ro
4. Storemap: Move controls UP (compact)
"""
import re

with open('index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# ============================
# 1. HEADER: Move "Giao dien + Cap nhat" to LEFT
# ============================
# Current: header has left side (logo/title) and right side (Giao dien + Cap nhat)
# Target: Put "Giao dien" and "Cap nhat" right next to the title, on the left

# Change header-right to be part of the left side
old_header = '''    <div class="header-right" style="display: flex; align-items: center; gap: 20px;">
        <button id="themeToggle" onclick="toggleTheme()" style="background: var(--bg2); border: 1px solid var(--border); color: var(--text); padding: 8px 12px; border-radius: var(--radius); cursor: pointer; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 6px; transition: all 0.2s;">
            <span id="themeIcon">☀️</span> Giao diện
        </button>'''

new_header = '''    <div class="header-right" style="display: flex; align-items: center; gap: 10px; margin-left: auto; margin-right: auto;">
        <button id="themeToggle" onclick="toggleTheme()" style="background: var(--bg2); border: 1px solid var(--border); color: var(--text); padding: 5px 10px; border-radius: var(--radius); cursor: pointer; font-size: 12px; font-weight: 600; display: flex; align-items: center; gap: 4px; transition: all 0.2s;">
            <span id="themeIcon">☀️</span> Giao diện
        </button>'''

if old_header in content:
    content = content.replace(old_header, new_header)
    print("[OK] Header: Moved Giao dien + Cap nhat to center-left")
else:
    print("[WARN] Header pattern not found, trying flexible match")
    # Try regex
    content = re.sub(
        r'(<div class="header-right" style="display: flex; align-items: center; gap:)\s*20px',
        r'\g<1> 10px; margin-left: auto; margin-right: auto',
        content
    )

# ============================  
# 2. TONKHO: Move filter-row + legend ABOVE stats-bar
# ============================
# Current order: stats-bar → filter-row → color-legend → table
# Target order: filter-row → color-legend → stats-bar → table

# Extract the sections
tonkho_match = re.search(
    r'(<div class="main-panel active" id="panel-tonkho">)\s*'
    r'(<div class="stats-bar">.*?</div>\s*</div>)\s*'  # stats-bar block (ends with nested </div>)
    r'(<div class="filter-row">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>)\s*'  # filter-row block
    r'(<div class="color-legend">.*?</div>)',  # color-legend
    content, re.DOTALL
)

if not tonkho_match:
    # Try a simpler approach: find the blocks by their unique IDs
    print("[INFO] Using block-swap approach for Tonkho")
    
    # Find stats-bar block
    stats_start = content.find('<div class="stats-bar">')
    filter_start = content.find('<div class="filter-row">', stats_start)
    legend_start = content.find('<div class="color-legend">', filter_start)
    table_start = content.find('<div class="table-wrap"', legend_start)
    
    if stats_start > 0 and filter_start > 0 and legend_start > 0 and table_start > 0:
        stats_block = content[stats_start:filter_start].strip()
        filter_block = content[filter_start:legend_start].strip()
        legend_block = content[legend_start:table_start].strip()
        
        # Get the panel opening
        panel_start = content.rfind('<div class="main-panel active" id="panel-tonkho">', 0, stats_start)
        panel_prefix = content[panel_start:stats_start].rstrip()
        
        # Rebuild: filter → legend → stats → table
        new_tonkho = panel_prefix + '\n    ' + filter_block + '\n    ' + legend_block + '\n    ' + stats_block + '\n    '
        
        content = content[:panel_start] + new_tonkho + content[table_start:]
        print("[OK] Tonkho: Moved filter-row + legend ABOVE stats-bar")
    else:
        print(f"[WARN] Tonkho blocks not found: stats={stats_start} filter={filter_start} legend={legend_start} table={table_start}")
else:
    print("[OK] Tonkho regex matched")

# ============================
# 3. THU HOI: Move calendar (cal-bar) ABOVE basket-summary
# ============================
# Current order: stats-bar → basket-summary → cal-bar → filter-row
# Target order: stats-bar → cal-bar → basket-summary → filter-row

# Find the blocks in thu hoi panel
thuhoi_start = content.find('id="panel-thuhoi"')
if thuhoi_start > 0:
    # Find basket-summary and cal-bar within thuhoi
    basket_start = content.find('<div class="basket-summary-panel"', thuhoi_start)
    cal_start = content.find('<div class="cal-bar"', thuhoi_start)
    filter_after_cal = content.find('<div class="filter-row">', cal_start)
    
    if basket_start > 0 and cal_start > 0 and filter_after_cal > 0:
        basket_block = content[basket_start:cal_start].strip()
        cal_block = content[cal_start:filter_after_cal].strip()
        
        # Swap: put cal-bar before basket-summary
        new_section = cal_block + '\n    ' + basket_block + '\n    '
        content = content[:basket_start] + new_section + content[filter_after_cal:]
        print("[OK] Thu hoi: Moved cal-bar ABOVE basket-summary")
    else:
        print(f"[WARN] Thu hoi blocks not found")

# ============================
# 4. STOREMAP: Reduce padding, compact controls
# ============================
# The storemap map-controls are already correctly structured
# Just reduce vertical spacing by making map-controls more compact
old_map_controls = '.map-controls { display:flex; flex-wrap:wrap; gap:12px; align-items:flex-end;'
new_map_controls = '.map-controls { display:flex; flex-wrap:wrap; gap:8px; align-items:flex-end;'
if old_map_controls in content:
    content = content.replace(old_map_controls, new_map_controls)
    print("[OK] Storemap: Reduced map-controls gap")
else:
    print("[SKIP] Storemap map-controls gap already compact or pattern different")

# Also reduce header padding to bring content closer to top
old_header_css = '.header { position:relative; z-index:9999; padding:24px 36px;'
new_header_css = '.header { position:relative; z-index:9999; padding:12px 24px;'
if old_header_css in content:
    content = content.replace(old_header_css, new_header_css)
    print("[OK] Header: Reduced padding (24px→12px, 36px→24px)")

# Reduce avatar size for more compact header
old_avatar = 'width="60" height="60"'
new_avatar = 'width="44" height="44"'
if old_avatar in content:
    content = content.replace(old_avatar, new_avatar, 1)
    print("[OK] Header: Reduced avatar size")

# Reduce container top padding
old_container = '.container { padding:20px 36px;'
new_container = '.container { padding:8px 24px;'
if old_container in content:
    content = content.replace(old_container, new_container)
    print("[OK] Container: Reduced top padding")
else:
    # Try alternate
    old_container2 = '.container { max-width:1800px; margin:0 auto; padding:20px 36px;'
    new_container2 = '.container { max-width:1800px; margin:0 auto; padding:8px 24px;'
    if old_container2 in content:
        content = content.replace(old_container2, new_container2)
        print("[OK] Container: Reduced top padding (alt)")

# Write back
with open('index.html', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("\n[DONE] All UI changes applied")
