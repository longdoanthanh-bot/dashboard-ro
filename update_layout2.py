import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

changed = False

# 1. Update panel-thuhoi
if 'id="panel-thuhoi"' in html and 'class="top-controls-thuhoi"' not in html:
    start_thuhoi = html.find('<div class="main-panel" id="panel-thuhoi">')
    start_stats = html.find('<div class="stats-bar compact">', start_thuhoi)
    start_cal = html.find('<div class="cal-bar" id="trip-date-bar">', start_thuhoi)
    start_filter = html.find('<div class="filter-row">', start_cal)
    start_legend = html.find('<div class="color-legend">', start_filter)
    start_summary = html.find('<div class="basket-summary-panel"', start_legend)
    
    if all(x != -1 for x in [start_thuhoi, start_stats, start_cal, start_filter, start_legend, start_summary]):
        stats_html = html[start_stats:start_cal].strip()
        cal_html = html[start_cal:start_filter].strip()
        filter_html = html[start_filter:start_legend].strip()
        legend_html = html[start_legend:start_summary].strip()
        
        stats_html = stats_html.replace('class="stats-bar compact"', 'class="stats-bar compact" style="margin-bottom: 0; flex: 1; min-width: 300px;"')
        cal_html = cal_html.replace('class="cal-bar"', 'class="cal-bar" style="margin-bottom: 0;"')
        filter_html = filter_html.replace('class="filter-row"', 'class="filter-row" style="margin-bottom: 0; justify-content: flex-end;"')
        legend_html = legend_html.replace('class="color-legend"', 'class="color-legend" style="margin-bottom: 0;"')
        
        new_header = f'''<div class="top-controls-thuhoi" style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px; margin-bottom: 12px;">
    {stats_html}
    <div class="filters-container-thuhoi" style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
        {cal_html}
        {filter_html}
        {legend_html}
    </div>
</div>
'''
        
        html = html[:start_stats] + new_header + html[start_summary:]
        print("Updated panel-thuhoi")
        changed = True

# 2. Update panel-storemap
if 'id="panel-storemap"' in html and 'class="map-controls-left"' not in html:
    start_storemap = html.find('<div class="main-panel" id="panel-storemap">')
    start_controls = html.find('<div class="map-controls">', start_storemap)
    start_legend = html.find('<div class="map-legend">', start_controls)
    
    if start_controls != -1 and start_legend != -1:
        controls_content = html[start_controls:start_legend]
        
        # split by elements
        # map-stats
        m_stats_start = controls_content.find('<div class="map-stats">')
        m_loc_start = controls_content.find('<div class="filter-group">\n            <span class="filter-label">Location Type</span>')
        m_distA_start = controls_content.find('<div class="filter-group">\n            <span class="filter-label">Đo KC: Điểm A</span>')
        
        if m_stats_start != -1 and m_loc_start != -1 and m_distA_start != -1:
            stats_html = controls_content[m_stats_start:m_loc_start].strip()
            filters_html = controls_content[m_loc_start:m_distA_start].strip()
            dist_html = controls_content[m_distA_start:].replace('</div>\n    ', '    ').strip() # remove trailing closing div of map-controls
            
            # The dist_html currently includes the closing div of map-controls
            # Let's fix that string
            dist_html = controls_content[m_distA_start:].strip()
            if dist_html.endswith('</div>'):
                dist_html = dist_html[:-6].strip()
            
            new_controls = f'''<div class="map-controls" style="display:flex; justify-content: space-between; width: 100%; align-items: flex-end;">
    <div class="map-controls-left" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-end;">
        {stats_html}
        {dist_html}
    </div>
    <div class="map-controls-right" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-end;">
        {filters_html}
    </div>
</div>
    '''
            html = html[:start_controls] + new_controls + html[start_legend:]
            print("Updated panel-storemap")
            changed = True

if changed:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Wrote changes to index.html")
else:
    print("No changes needed")
