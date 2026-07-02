import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_sm = html.find('<div class="main-panel" id="panel-storemap">')
if start_sm != -1:
    end_sm = html.find('</div>\n    <div class="map-legend">', start_sm)
    if end_sm != -1:
        chunk = html[start_sm:end_sm+6]
        
        # Left block (contains map-stats, currently has class map-controls-right and justify-content: flex-end;)
        left_match = re.search(r'<div class="map-controls-right" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-end; justify-content: flex-end;">\n        <div class="map-stats">.*?</div>\n    </div>', chunk, re.DOTALL)
        
        # Right block (contains map-loc-filter, currently has class map-controls-right without justify-content)
        right_match = re.search(r'<div class="map-controls-right" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-end;">\n        <div class="filter-group">\n            <span class="filter-label">Location Type</span>.*?</div>\n    </div>', chunk, re.DOTALL)
        
        if left_match and right_match:
            left_html = left_match.group(0).replace('class="map-controls-right"', 'class="map-controls-left"').replace(' justify-content: flex-end;', '')
            right_html = right_match.group(0).replace('align-items: flex-end;"', 'align-items: flex-end; justify-content: flex-end;"')
            
            new_chunk = f'''<div class="main-panel" id="panel-storemap">
    <div class="map-controls" style="display: flex; flex-direction: column; align-items: flex-end; padding-left: 450px; gap: 12px; margin-bottom: 12px; min-height: 80px; position: relative; z-index: 10;">
    {right_html}
    {left_html}
</div>'''
            html = html.replace(chunk, new_chunk)
            
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("Fixed panel-storemap")
        else:
            print("Regex did not match")
