import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Push Theme toggle & Update time to the right
if 'margin-left: auto;' not in html.split('id="themeToggle"')[1][:200]:
    html = re.sub(
        r'(<button id="themeToggle"[^>]*style=")',
        r'\1margin-left: auto; ',
        html,
        count=1
    )
    print("Added margin-left: auto to themeToggle")

# 2. Swap Stats Bar and Filter Row to be side-by-side
if 'class="top-controls"' not in html:
    start_filter = html.find('<div class="filter-row">')
    start_legend = html.find('<div class="color-legend">')
    start_stats = html.find('<div class="stats-bar">')
    start_table = html.find('<div class="table-wrap"')
    
    if start_filter != -1 and start_legend != -1 and start_stats != -1 and start_table != -1:
        filter_html = html[start_filter:start_legend]
        legend_html = html[start_legend:start_stats]
        stats_html = html[start_stats:start_table]
        
        # Add flex styles to remove their bottom margins to let top-controls handle it
        stats_html = stats_html.replace('class="stats-bar"', 'class="stats-bar" style="margin-bottom: 0; flex: 1; min-width: 450px;"')
        filter_html = filter_html.replace('class="filter-row"', 'class="filter-row" style="margin-bottom: 0; justify-content: flex-end;"')
        
        new_header = f'''<div class="top-controls" style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px; margin-bottom: 12px;">
    {stats_html.strip()}
    <div class="filters-container" style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
        {filter_html.strip()}
        {legend_html.strip()}
    </div>
</div>
'''
        
        html = html[:start_filter] + new_header + html[start_table:]
        print("Rearranged panel-tonkho layout")
    else:
        print("Could not find one of the blocks to rearrange")
else:
    print("Already rearranged")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
