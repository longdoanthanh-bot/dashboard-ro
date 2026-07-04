import re

def fix_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update global header
    # Original header:
    # <header class="header">
    #     <div style="position: relative; display: flex; align-items: center; gap: 14px; flex-wrap:wrap;" id="navMenuContainer"> ... </div>
    #     <div style="display: flex; align-items: center; gap: 14px;"> ... </div>
    # </header>
    
    header_pattern = r'<header class="header">(.*?)</header>'
    match = re.search(header_pattern, html, re.DOTALL)
    if match:
        h_content = match.group(1)
        # We want to change the second div to have padding-left: 74px
        h_content = h_content.replace('<div style="display: flex; align-items: center; gap: 14px;">', 
                                      '<div style="display: flex; align-items: center; gap: 14px; padding-left: 74px;">')
        
        new_header = f'<header class="header" style="position: absolute; top: 16px; left: 36px; z-index: 100; display: flex; flex-direction: column; gap: 8px; align-items: flex-start; padding: 0; border: none; background: transparent;">{h_content}</header>'
        html = html.replace(match.group(0), new_header)

    # We also need to add padding-top to .container so the table doesn't hit the top if controls are short.
    # Actually, .container padding is already `padding: 0 36px 24px;` ( wait, earlier I changed it to max-width: 100% )
    html = html.replace('.container { position:relative; z-index:1; max-width:100%; margin:0 auto; padding:0 36px 24px; }',
                        '.container { position:relative; z-index:1; max-width:100%; margin:0 auto; padding:16px 36px 24px; }')

    if file_path == 'index.html':
        # panel-tonkho
        tk_ctrl_match = re.search(r'<div class="top-controls" style=".*?">(.*?)<div class="filters-container".*?>(.*?)</div>\n    </div>', html, re.DOTALL)
        if tk_ctrl_match:
            # We want to swap stats and filters
            # Currently it is: <div class="stats-bar"...></div> <div class="filters-container"...></div>
            # Wait, my regex might not capture it correctly.
            pass
            
        # Let's do it with precise string manipulation
        # Ton kho
        start_tk = html.find('<div class="top-controls" style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px; margin-bottom: 12px;">')
        if start_tk != -1:
            end_tk = html.find('</div>\n    </div>\n</div>\n<div class="table-wrap"', start_tk)
            if end_tk != -1:
                # end_tk is before the closing </div> of top-controls
                # Let's just find the exact chunks
                chunk = html[start_tk:end_tk+14]
                stats_chunk = re.search(r'<div class="stats-bar" .*?</div>\n    </div>', chunk, re.DOTALL).group(0)
                filters_chunk = re.search(r'<div class="filters-container".*?</div>\n    </div>', chunk, re.DOTALL).group(0)
                
                new_chunk = f'''<div class="top-controls" style="display: flex; flex-direction: column; align-items: flex-end; padding-left: 350px; gap: 12px; margin-bottom: 12px; min-height: 80px;">
    {filters_chunk}
    {stats_chunk.replace("flex: 1; min-width: 450px;", "")}
</div>'''
                html = html.replace(chunk, new_chunk)
        
        # Thu hoi
        start_th = html.find('<div class="top-controls-thuhoi"')
        if start_th != -1:
            end_th = html.find('</div>\n    </div>\n</div>\n<div class="table-wrap"', start_th)
            if end_th != -1:
                chunk = html[start_th:end_th+14]
                stats_chunk = re.search(r'<div class="stats-bar compact" .*?</div>\n    </div>', chunk, re.DOTALL).group(0)
                filters_chunk = re.search(r'<div class="filters-container-thuhoi".*?</div>\n    </div>\n    </div>', chunk, re.DOTALL)
                if not filters_chunk:
                    filters_chunk = re.search(r'<div class="filters-container-thuhoi".*?<div class="color-legend".*?</div>', chunk, re.DOTALL).group(0)
                else:
                    filters_chunk = filters_chunk.group(0)
                
                new_chunk = f'''<div class="top-controls-thuhoi" style="display: flex; flex-direction: column; align-items: flex-end; padding-left: 350px; gap: 12px; margin-bottom: 12px; min-height: 80px;">
    {filters_chunk}
    {stats_chunk.replace("flex: 1; min-width: 300px;", "")}
</div>'''
                html = html.replace(chunk, new_chunk)

        # Storemap
        start_sm = html.find('<div class="map-controls"')
        if start_sm != -1:
            end_sm = html.find('</div>\n    <div class="map-legend">', start_sm)
            if end_sm != -1:
                chunk = html[start_sm:end_sm+6]
                left_chunk = re.search(r'<div class="map-controls-left".*?(?=<div class="map-controls-right")', chunk, re.DOTALL).group(0)
                right_chunk = re.search(r'<div class="map-controls-right".*?</div>', chunk, re.DOTALL).group(0)
                
                new_chunk = f'''<div class="map-controls" style="display: flex; flex-direction: column; align-items: flex-end; padding-left: 350px; gap: 12px; margin-bottom: 12px; min-height: 80px;">
    {right_chunk}
    {left_chunk}
</div>'''
                html = html.replace(chunk, new_chunk)

    if file_path == 'tasks.html':
        start_tasks = html.find('<div class="top-row"')
        if start_tasks != -1:
            end_tasks = html.find('</div>\n    </div>\n    \n    <div class="board">', start_tasks)
            if end_tasks != -1:
                chunk = html[start_tasks:end_tasks+12]
                form_chunk = re.search(r'<div class="add-task-form".*?(?=<div class="stats-group")', chunk, re.DOTALL).group(0)
                stats_chunk = re.search(r'<div class="stats-group".*?</div>\n    </div>', chunk, re.DOTALL).group(0)
                
                new_chunk = f'''<div class="top-row" style="display: flex; flex-direction: column; align-items: flex-end; padding-left: 350px; gap: 12px; margin-bottom: 16px; min-height: 80px;">
    {form_chunk.replace("margin-left: auto;", "")}
    {stats_chunk.replace("flex: 1;", "")}
</div>'''
                html = html.replace(chunk, new_chunk)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated {file_path}")

fix_html('index.html')
fix_html('tasks.html')
