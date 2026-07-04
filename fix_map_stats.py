def fix_map_stats():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Move map-stats to the left
    
    old_map_left = """    <div class="map-controls-left" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: center; justify-content: flex-start;">
        <div class="map-stats">
            <div class="map-stat"><div class="map-stat-num" style="color:var(--blue)" id="map-total">0</div><div class="map-stat-label">Tổng ST</div></div>
            <div class="map-stat"><div class="map-stat-num" style="color:var(--green)" id="map-mart">0</div><div class="map-stat-label">Mart</div></div>
            <div class="map-stat"><div class="map-stat-num" style="color:var(--purple)" id="map-mini">0</div><div class="map-stat-label">Mini</div></div>
        </div>
        <div class="filter-group">"""

    new_map_left = """    <!-- MAP STATS MOVED TO LEFT -->
    <div class="map-stats" style="position: absolute; left: 12px; top: 110px; width: 380px; z-index: 20; justify-content: flex-start;">
        <div class="map-stat"><div class="map-stat-num" style="color:var(--blue)" id="map-total">0</div><div class="map-stat-label">Tổng ST</div></div>
        <div class="map-stat"><div class="map-stat-num" style="color:var(--green)" id="map-mart">0</div><div class="map-stat-label">Mart</div></div>
        <div class="map-stat"><div class="map-stat-num" style="color:var(--purple)" id="map-mini">0</div><div class="map-stat-label">Mini</div></div>
    </div>
    
    <div class="map-controls-left" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: center; justify-content: flex-start;">
        <div class="filter-group">"""

    html = html.replace(old_map_left, new_map_left)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    fix_map_stats()
