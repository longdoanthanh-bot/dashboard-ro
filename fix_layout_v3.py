import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Storemap Header Filters
# The user wants all map controls in the header, stacked vertically.
# storemap-header-filters in fb12a2d currently contains <div class="map-controls">.
# We need to change its style to flex-direction: column.
storemap_header_match = re.search(r'<div id="storemap-header-filters" class="header-filters" style="(.*?)">', c)
if storemap_header_match:
    old_style = storemap_header_match.group(1)
    new_style = "flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: center; gap: 4px;"
    c = c.replace(f'<div id="storemap-header-filters" class="header-filters" style="{old_style}">', f'<div id="storemap-header-filters" class="header-filters" style="{new_style}">')

# Find the filter-row (Do KC) and map-legend in panel-storemap and move them to storemap-header-filters
panel_sm_idx = c.find('<div class="main-panel" id="panel-storemap">')
if panel_sm_idx != -1:
    filter_row_match = re.search(r'(\s*<div class="filter-row".*?</div>\s*</div>\s*</div>\s*</div>)', c[panel_sm_idx:], re.DOTALL)
    map_legend_match = re.search(r'(\s*<div class="map-legend">.*?</div>)', c[panel_sm_idx:], re.DOTALL)
    
    # Wait, using regex might be fragile, let's just find them by index and split properly.
