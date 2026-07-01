import re

with open('oldest_index.html', 'r', encoding='utf-8') as f:
    old_c = f.read()

# Extract from oldest_index.html
# It is between <div class="map-controls"> and <div class="map-legend">
match = re.search(r'(<div class="map-controls">.*?)(?=\s*<div class="map-legend">)', old_c, re.DOTALL)
if match:
    full_map_controls = match.group(1)
    
    with open('index.html', 'r', encoding='utf-8') as f:
        c = f.read()
        
    # Find the broken map-controls in index.html
    # It might be: <div class="map-controls" style="..."> ... </div>
    # and maybe some other broken things
    broken_match = re.search(r'<div class="map-controls".*?</div>\s*(<div class="filter-row")', c, re.DOTALL)
    if broken_match:
        # We replace the broken map-controls with the full one
        # And also apply the horizontal styling "dàn đều ngang"
        styled_map_controls = full_map_controls.replace('class="map-controls"', 'class="map-controls" style="display:flex; flex-direction:row; align-items:flex-end; gap:12px; flex-wrap:nowrap; overflow-x:auto; width:100%;"')
        c = c[:broken_match.start()] + styled_map_controls + '\n    ' + broken_match.group(1) + c[broken_match.end(1):]
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(c)
        print("Restored map-controls successfully.")
    else:
        print("Could not find broken map-controls in index.html")
else:
    print("Could not find map-controls in oldest_index.html")
