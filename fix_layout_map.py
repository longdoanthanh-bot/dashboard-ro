import re

def fix_map_layout():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    pattern = re.compile(r'<div class="map-controls".*?<!-- MAP STATS MOVED TO LEFT -->\s*<div class="map-stats".*?</div>\s*</div>\s*<div class="map-controls-left".*?</div>\s*</div>\s*<div class="map-legend">.*?</div>', re.DOTALL)
    
    match = pattern.search(html)
    if not match:
        print("Map controls not found!")
        return

    map_controls_right = """
        <div class="filter-group">
            <span class="filter-label">Location Type</span>
            <select class="filter-select" id="map-loc-filter" onchange="filterMap()">
                <option value="">Tất cả</option>
                <option value="STREAM">STREAM</option>
                <option value="LAKE">LAKE</option>
                <option value="RIVER">RIVER</option>
                <option value="LAKE-S">LAKE-S</option>
                <option value="LAKE-M">LAKE-M</option>
            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">Doanh thu</span>
            <select class="filter-select" id="map-rev-filter" onchange="filterMap()">
                <option value="">Tất cả</option>
                <option value="A">A (>4B)</option>
                <option value="B">B (2-4B)</option>
                <option value="C">C (<2B)</option>
            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">Tìm kiếm ST <span class="tag-counter" id="tag-counter"></span></span>
            <div class="tag-input-wrap">
                <div class="tag-input-box" id="tag-box" onclick="document.getElementById('tag-input').focus()">
                    <input type="text" id="tag-input" placeholder="Gõ mã ST, Enter để thêm (tối đa 10)" autocomplete="off"
                        oninput="this.value=this.value.toUpperCase();tagSuggest()" onkeydown="tagKeydown(event)" onfocus="tagSuggest()">
                </div>
                <div class="tag-suggest" id="tag-suggest-list"></div>
            </div>
        </div>
        <div class="filter-group">
            <span class="filter-label">Lân cận</span>
            <select class="filter-select" id="map-nearby-n" onchange="filterMap()">
                <option value="0">Chỉ ST</option>
                <option value="5" selected>Top 5</option>
                <option value="10">Top 10</option>
            </select>
        </div>
    """

    map_controls_left = """
        <div class="filter-group">
            <span class="filter-label">Đo KC: Điểm A</span>
            <div class="combo-wrap">
                <input class="filter-select search-upper" type="text" id="dist-a" placeholder="Gõ mã ST..." autocomplete="off" oninput="this.value=this.value.toUpperCase();comboFilter('dist-a')" onfocus="comboFilter('dist-a')">
                <div class="combo-list" id="dist-a-list"></div>
            </div>
        </div>
        <div class="filter-group">
            <span class="filter-label">Điểm B</span>
            <div class="combo-wrap">
                <input class="filter-select search-upper" type="text" id="dist-b" placeholder="Gõ mã ST..." autocomplete="off" oninput="this.value=this.value.toUpperCase();comboFilter('dist-b')" onfocus="comboFilter('dist-b')">
                <div class="combo-list" id="dist-b-list"></div>
            </div>
        </div>
        <button class="btn-export" onclick="calcDistance()" style="padding:6px 14px;font-size:11px;align-self:flex-end;">📏 Tính KC</button>
        <div id="dist-result" style="align-self:center;padding:6px 12px;font-size:12px;color:var(--green);font-weight:600;"></div>
    """

    legend = """
    <div class="map-legend" style="margin-bottom: 0;">
        <span class="map-legend-title">Doanh thu:</span>
        <span class="ml-item"><span class="ml-dot" style="background:#34d399"></span> A (>4B)</span>
        <span class="ml-item"><span class="ml-dot" style="background:#6c8cff"></span> B (2-4B)</span>
        <span class="ml-item"><span class="ml-dot" style="background:#9898b0"></span> C (<2B)</span>
        <span style="color:var(--border)">|</span>
        <span class="map-legend-title">Loại:</span>
        <span class="ml-item"><span class="ml-dot lg" style="background:#fb923c"></span> Mart</span>
        <span class="ml-item"><span class="ml-dot sm" style="background:#a78bfa"></span> Mini</span>
    </div>
    <button class="btn-export" onclick="exportMapExcel()" style="padding:6px 14px;font-size:11px;align-self:center;">&#x1F4E5; Xuất Excel</button>
    """

    stats = """
        <div class="map-stat"><div class="map-stat-num" style="color:var(--blue)" id="map-total">0</div><div class="map-stat-label">Tổng ST</div></div>
        <div class="map-stat"><div class="map-stat-num" style="color:var(--green)" id="map-mart">0</div><div class="map-stat-label">Mart</div></div>
        <div class="map-stat"><div class="map-stat-num" style="color:var(--purple)" id="map-mini">0</div><div class="map-stat-label">Mini</div></div>
    """

    new_map = f"""<div class="map-controls" style="display: flex; flex-direction: column; align-items: stretch; justify-content: flex-start; padding-left: 0; flex-wrap: nowrap; gap: 8px; margin-bottom: 12px; position: relative; z-index: 10;">
    <!-- Row 1: Logo Space + Filters Right -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: nowrap; align-items: flex-start; width: 100%;">
        <div style="width: 420px; flex-shrink: 0; min-height: 50px;"></div>
        <div style="display: flex; flex-direction: row; align-items: flex-end; flex-wrap: wrap; gap: 12px; flex: 1;">
            {map_controls_right}
        </div>
    </div>

    <!-- Row 2: Filters Left + Legend + Excel -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: nowrap; align-items: flex-start; width: 100%;">
        <div style="width: 420px; flex-shrink: 0; min-height: 40px;"></div>
        <div style="display: flex; flex-direction: row; align-items: flex-end; flex-wrap: wrap; gap: 12px; flex: 1;">
            {map_controls_left}
            <div style="flex-grow: 1;"></div>
            {legend}
        </div>
    </div>

    <!-- Row 3: Stats Block on left -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: nowrap; width: 100%;">
        <div class="map-stats" style="width: 420px; flex-shrink: 0; justify-content: flex-start; gap: 8px; padding-left: 12px; margin-bottom: 0;">
            {stats}
        </div>
        <div style="flex: 1;"></div>
    </div>
</div>"""

    html = html[:match.start()] + new_map + html[match.end():]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    fix_map_layout()
