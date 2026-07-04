import re

def refactor_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Extract Header content
    start_header = html.find('<header class="header">')
    end_header = html.find('</header>') + len('</header>')
    header_html = html[start_header:end_header]
    
    # Modify header HTML to remove flex-row behavior and stack items
    # Original header has a div for navMenuContainer and a div for themeToggle
    # We will rewrite the header
    new_header = '''<header class="header" style="display: flex; flex-direction: column; gap: 12px; align-items: flex-start; margin-bottom: 0; padding: 0; border: none; width: auto; position: relative; z-index: 10;">
    <div style="position: relative; display: flex; align-items: center; gap: 14px; flex-wrap:wrap;" id="navMenuContainer">
        <img src="./avatar.png?v=4" width="60" height="60" style="border-radius: 50%; object-fit: cover; cursor: pointer; box-shadow: 0 4px 18px rgba(249, 115, 22, 0.6); border: 2px solid #f97316; transition: transform 0.2s; filter: contrast(1.15) saturate(1.2);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" onclick="toggleNavMenu()" alt="Trợ lý">
        <h1 style="margin: 0; font-size: 24px; font-weight: 800;">
            <span style="background: linear-gradient(135deg, #f97316, #fb923c); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Trợ lý — KingFoodmart</span>
        </h1>
        <div id="navMenuDropdown" style="display: none; position: absolute; top: 100%; left: 0; margin-top: 15px; background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 8px; min-width: 260px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); z-index: 9999;">
            <div class="nav-menu-item active" onclick="selectNavMenu(event, 'tonkho', 'Trợ lý — KingFoodmart')">📊 Tồn Rổ tại Siêu Thị</div>
            <div class="nav-menu-item" onclick="selectNavMenu(event, 'thuhoi', 'Trợ lý — KingFoodmart')">🔄 Tiến Độ Thu Hồi</div>
            <div class="nav-menu-item" onclick="selectNavMenu(event, 'storemap', 'Trợ lý — KingFoodmart')">🗺️ Sơ Đồ ST</div>
            <div class="nav-menu-item" onclick="selectNavMenu(event, 'tasks', 'Trợ lý — KingFoodmart')">📋 Công Việc</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 14px; padding-left: 74px;">
        <button id="themeToggle" onclick="toggleTheme()" style=" background: var(--bg2); border: 1px solid var(--border); color: var(--text); padding: 6px 10px; border-radius: var(--radius); cursor: pointer; font-size: 12px; font-weight: 600; display: flex; align-items: center; gap: 5px; transition: all 0.2s;">
            <span id="themeIcon">☀️</span> Giao diện
        </button>
        <div style="font-size:11px; color:var(--text3);">Cập nhật: 01/07/2026 22:46</div>
    </div>
</header>'''

    # Extract Ton kho controls
    start_tk_ctrl = html.find('<div class="top-controls-tonkho"')
    end_tk_ctrl = html.find('</div>\n</div>\n<div class="table-wrap"')
    if end_tk_ctrl == -1: end_tk_ctrl = html.find('<div class="table-wrap"', start_tk_ctrl)
    
    # We need to precisely grab the div
    # Actually let's use regex or string finding carefully
    # In index.html, tonkho controls ends before <div class="table-wrap"
    end_tk_ctrl = html.find('<div class="table-wrap"', start_tk_ctrl)
    tk_ctrl_html = html[start_tk_ctrl:end_tk_ctrl]
    # Remove it from html
    html = html[:start_tk_ctrl] + html[end_tk_ctrl:]
    
    # Extract Thu hoi controls
    start_th_ctrl = html.find('<div class="top-controls-thuhoi"')
    end_th_ctrl = html.find('<div class="table-wrap"', start_th_ctrl)
    th_ctrl_html = html[start_th_ctrl:end_th_ctrl]
    html = html[:start_th_ctrl] + html[end_th_ctrl:]
    
    # Extract Storemap controls
    start_sm_ctrl = html.find('<div class="map-controls"')
    end_sm_ctrl = html.find('<div class="map-legend">', start_sm_ctrl)
    sm_ctrl_html = html[start_sm_ctrl:end_sm_ctrl]
    html = html[:start_sm_ctrl] + html[end_sm_ctrl:]
    
    # Transform controls to have Filters on top, Stats below
    # Ton kho
    tk_stats = re.search(r'<div class="stats-bar compact".*?(?=<div class="filters-container)', tk_ctrl_html, re.DOTALL)
    tk_filters = re.search(r'<div class="filters-container".*?</div>\n    </div>', tk_ctrl_html, re.DOTALL)
    if tk_stats and tk_filters:
        tk_new = f'''<div id="controls-tonkho" class="tab-controls-group" style="display: flex; flex-direction: column; align-items: flex-end; gap: 12px; width: 100%;">
    {tk_filters.group(0).replace('margin-bottom: 0;', '')}
    {tk_stats.group(0).replace('flex: 1; min-width: 300px;', '')}
</div>'''
    else:
        print("Failed to parse tk")
        return
        
    # Thu hoi
    th_stats = re.search(r'<div class="stats-bar compact".*?(?=<div class="filters-container-thuhoi)', th_ctrl_html, re.DOTALL)
    th_filters = re.search(r'<div class="filters-container-thuhoi".*?</div>\n    </div>\n    </div>', th_ctrl_html, re.DOTALL)
    if not th_filters: # fallback
        th_filters = re.search(r'<div class="filters-container-thuhoi".*?<div class="color-legend".*?</div>', th_ctrl_html, re.DOTALL)
    
    if th_stats and th_filters:
        th_new = f'''<div id="controls-thuhoi" class="tab-controls-group" style="display: none; flex-direction: column; align-items: flex-end; gap: 12px; width: 100%;">
    {th_filters.group(0)}
    {th_stats.group(0).replace('flex: 1; min-width: 300px;', '')}
</div>'''
    else:
        print("Failed to parse th")
        return

    # Storemap
    sm_stats = re.search(r'<div class="map-controls-left".*?(?=<div class="map-controls-right")', sm_ctrl_html, re.DOTALL)
    sm_filters = re.search(r'<div class="map-controls-right".*?</div>', sm_ctrl_html, re.DOTALL)
    if sm_stats and sm_filters:
        sm_new = f'''<div id="controls-storemap" class="tab-controls-group" style="display: none; flex-direction: column; align-items: flex-end; gap: 12px; width: 100%;">
    {sm_filters.group(0)}
    {sm_stats.group(0)}
</div>'''
    else:
        print("Failed to parse sm")
        return

    # Build the new page-top block
    page_top_html = f'''
<div class="page-top" style="display: flex; justify-content: space-between; align-items: flex-start; padding: 16px 36px 0; gap: 20px; max-width: 100%; margin: 0 auto;">
    {new_header}
    <div class="global-tab-controls" style="flex: 1; display: flex; justify-content: flex-end; min-width: 0;">
        {tk_new}
        {th_new}
        {sm_new}
    </div>
</div>
'''
    
    # Replace the old header with the new page-top block
    html = html.replace(header_html, page_top_html)
    
    # Inject JS into selectNavMenu to toggle controls
    js_addition = '''
    // Toggle controls
    document.querySelectorAll('.tab-controls-group').forEach(el => el.style.display = 'none');
    const activeControls = document.getElementById('controls-' + tabId);
    if (activeControls) activeControls.style.display = 'flex';
'''
    html = html.replace("document.getElementById('panel-' + tabId).classList.add('active');", 
                        "document.getElementById('panel-' + tabId).classList.add('active');" + js_addition)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Refactored index.html")

refactor_index()
