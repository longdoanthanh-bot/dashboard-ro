import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Extract map-controls and remove from index.html header
map_match = re.search(r'(<div class="map-controls">.*?</div>\s*</div>\s*</div>)', c, re.DOTALL)
if map_match:
    map_html = map_match.group(1)
    # Remove from tasks-header-filters? No, map-controls is in storemap-header-filters
    c = c.replace(map_html, '')
    
    # Let's fix the map_html to be "dàn đều" (flex-row, nowrap)
    # Wait, the best way to dàn đều is to add CSS or style directly
    map_html_fixed = map_html.replace('class="map-controls"', 'class="map-controls" style="display:flex; flex-direction:row; align-items:flex-end; gap:12px; flex-wrap:nowrap; overflow-x:auto; width:100%;"')
    
    # Insert back into panel-storemap before the filter-row
    # In index.html, look for <div class="main-panel" id="panel-storemap">
    panel_idx = c.find('<div class="main-panel" id="panel-storemap">')
    if panel_idx != -1:
        insert_idx = c.find('<div class="filter-row"', panel_idx)
        if insert_idx != -1:
            c = c[:insert_idx] + map_html_fixed + '\n    ' + c[insert_idx:]

# 2. Extract add-form from index.html header
add_form_match = re.search(r'(<div class="add-form">.*?</div>\s*</div>)', c, re.DOTALL)
if add_form_match:
    add_form_html = add_form_match.group(1)
    # Remove from index.html
    c = c.replace(add_form_html, '')
    
    # Fix add_form_html to be "dàn đều"
    # Actually, add_form_html already has the style in CSS or we can inject it inline
    
    with open('tasks.html', 'r', encoding='utf-8') as tf:
        tc = tf.read()
    
    # Update tasks.html CSS for .add-form to ensure it's dàn đều
    old_css = ".add-form {\n    flex:1; background:var(--card); border:1px solid var(--border); border-radius:8px;\n    padding:8px 14px; display:flex; align-items:flex-end; gap:10px; flex-wrap:wrap;\n}"
    new_css = ".add-form {\n    flex:1; background:transparent; padding:0; display:flex; align-items:flex-end; gap:12px; flex-wrap:nowrap; overflow-x:auto;\n}\n.add-form .form-title { white-space:nowrap; margin-right:8px; }\n.add-form .form-group { white-space:nowrap; }"
    tc = tc.replace(old_css, new_css)
    
    # Insert add_form_html into top-row of tasks.html
    top_row_idx = tc.find('<div class="top-row"')
    if top_row_idx != -1:
        # Find the closing > of the top-row div
        closing_bracket = tc.find('>', top_row_idx)
        if closing_bracket != -1:
            tc = tc[:closing_bracket+1] + '\n        ' + add_form_html + tc[closing_bracket+1:]
    
    # Clean up the buttons since they are now back inside iframe!
    # They were: onclick="document.getElementById('iframe-tasks').contentWindow.createTask()"
    # Change back to onclick="createTask()"
    tc = tc.replace("document.getElementById('iframe-tasks').contentWindow.createTask()", "createTask()")
    tc = tc.replace("document.getElementById('iframe-tasks').contentWindow.exportExcel()", "exportExcel()")
    
    with open('tasks.html', 'w', encoding='utf-8') as tf:
        tf.write(tc)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Restored!")
