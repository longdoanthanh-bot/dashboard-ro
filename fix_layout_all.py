import re

def fix_all_layouts():
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_html = f.read()

    # 1. Thu Hồi
    match_th = re.search(r'<div class="top-controls" id="thuhoi-controls"([^>]*)>(.*?)<!-- STATS MOVED TO LEFT -->\s*<div class="stats-bar compact"(.*?)>(.*?)</div>', idx_html, re.DOTALL)
    if match_th:
        top_attrs = match_th.group(1).replace('padding-left: 420px;', 'padding-left: 0;')
        # We know Thu Hồi has specific filters
        filters_html = """
        <div class="filter-group">
            <span class="filter-label">Tìm ST</span>
            <div class="search-wrap">
                <input class="filter-select search-upper" type="text" id="th-search" placeholder="Gõ tên hoặc mã ST..." autocomplete="off" oninput="this.value=this.value.toUpperCase();filterThuHoi()">
                <button class="search-clear" onclick="clearSearch('th-search','filterThuHoi')">&times;</button>
            </div>
        </div>
        <div class="filter-group">
            <span class="filter-label">Lọc trạng thái</span>
            <select class="filter-select" id="th-status" onchange="filterThuHoi()">
                <option value="">Tất cả</option>
                <option value="miss">Chưa thu / Thiếu</option>
                <option value="ok">Đủ / Dư</option>
            </select>
        </div>"""
        
        legend_html = """
        <div class="color-legend" style="margin-bottom: 0;">
            <span class="legend-title">Chênh lệch:</span>
            <span class="legend-item"><span class="legend-dot ld-green"></span>0 (đủ)</span>
            <span class="legend-item"><span class="legend-dot ld-yellow"></span>&lt; 10</span>
            <span class="legend-item"><span class="legend-dot ld-orange"></span>10 – 30</span>
            <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 30</span>
        </div>"""
        
        stats_content = match_th.group(4)
        
        new_thuhoi = f"""<div class="top-controls" id="thuhoi-controls"{top_attrs}>
    <!-- Row 1: Logo Space + Filters + Legend -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: nowrap; align-items: flex-start; width: 100%;">
        <div style="width: 420px; flex-shrink: 0; min-height: 70px;"></div>
        
        <div style="display: flex; flex-direction: row; align-items: flex-end; flex-wrap: wrap; gap: 12px; flex: 1;">
            {filters_html}
            <div style="flex-grow: 1;"></div>
            {legend_html}
        </div>
    </div>

    <!-- Row 2: Stats Block on left -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: nowrap; width: 100%;">
        <div class="stats-bar compact" style="width: 420px; flex-shrink: 0; justify-content: flex-start; gap: 8px; padding-left: 12px; margin-bottom: 0;">
            {stats_content}
        </div>
        <div style="flex: 1;"></div>
    </div>"""
        idx_html = idx_html[:match_th.start()] + new_thuhoi + idx_html[match_th.end():]


    # 2. Sơ Đồ
    # It has <div class="map-controls" ...>
    # <div class="map-controls-left"...> and <div class="map-controls-right"...>
    # Wait, my previous script changed Sơ Đồ. Let's look for <!-- MAP STATS MOVED TO LEFT -->
    match_map = re.search(r'<!-- MAP STATS MOVED TO LEFT -->\s*<div class="map-stats"(.*?)>(.*?)</div>\s*<div class="map-controls-left"(.*?)>(.*?)</div>\s*<div class="map-controls-right"(.*?)>(.*?)</div>', idx_html, re.DOTALL)
    # Actually my previous script put MAP STATS MOVED TO LEFT outside map-controls?
    # Let me check.
    pass # I'll do Map and Tasks in a separate step to verify their exact content.

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx_html)

if __name__ == '__main__':
    fix_all_layouts()
