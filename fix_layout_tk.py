import re

def fix_layout():
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_html = f.read()

    # 1. Tồn Kho
    match_tk = re.search(r'<div class="top-controls"([^>]*)>(.*?)<!-- STATS MOVED TO LEFT -->\s*<div class="stats-bar"(.*?)>(.*?)</div>', idx_html, re.DOTALL)
    if match_tk:
        top_attrs = match_tk.group(1).replace('padding-left: 420px;', 'padding-left: 0;')
        filters_content = match_tk.group(2)
        stats_attrs = match_tk.group(3)
        stats_content = match_tk.group(4)

        # Extract filters and legend from filters_content
        # It currently looks like:
        # <div class="filters-container"...>
        #   <div class="filter-row"...>
        #     <div class="filter-group">...</div> x4
        #   </div>
        #   <div style="...">
        #     <div class="color-legend">...</div>
        #   </div>
        # </div>
        
        # We will just rewrite the whole top-controls content
        filters_html = """
        <div class="filter-group">
            <span class="filter-label">Kho</span>
            <select class="filter-select" id="tonkho-wh-filter" onchange="filterWarehouse(this.value)">
                <option value="">Tất cả</option>
<option value="Khô">Khô</option>
<option value="Rau">Rau</option>
<option value="Đông Mát">Đông Mát</option>

            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">Hiển thị</span>
            <select class="filter-select" id="tonkho-top-filter" onchange="filterTop(+this.value)">
                <option value="10">Top 10</option><option value="20">Top 20</option>
                <option value="50">Top 50</option><option value="100">Top 100</option>
                <option value="9999" selected>Tất cả</option>
            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">Lọc rổ</span>
            <div class="dropdown-wrap" id="col-filters">
                <button class="filter-select dropdown-btn" type="button" onclick="toggleDD('col-dd')">Tất cả</button>
                <div class="dropdown-panel" id="col-dd"><label class="dd-item"><input type="checkbox" checked onchange="toggleColCheck(-1,this)"> Tất cả</label>
<label class="dd-item" data-warehouse="Đông Mát"><input type="checkbox" checked data-col="0" data-warehouse="Đông Mát" onchange="toggleColCheck(0,this)"> ITL Thùng tote xanh dương</label>
<label class="dd-item" data-warehouse="Rau"><input type="checkbox" checked data-col="1" data-warehouse="Rau" onchange="toggleColCheck(1,this)"> Rổ nhựa đen/xanh lá kho r</label>
<label class="dd-item" data-warehouse="Khô"><input type="checkbox" checked data-col="2" data-warehouse="Khô" onchange="toggleColCheck(2,this)"> Seedlog - Thùng tote xanh</label>
<label class="dd-item" data-warehouse="Rau"><input type="checkbox" checked data-col="3" data-warehouse="Rau" onchange="toggleColCheck(3,this)"> Rổ đen xếp chồng quai đỏ</label>
<label class="dd-item" data-warehouse="Đông Mát"><input type="checkbox" checked data-col="4" data-warehouse="Đông Mát" onchange="toggleColCheck(4,this)"> Rổ nhựa đỏ kích thước 60x</label>
<label class="dd-item" data-warehouse=""><input type="checkbox" checked data-col="5" data-warehouse="" onchange="toggleColCheck(5,this)"> Rổ cam xếp chồng quai đỏ </label>
<label class="dd-item" data-warehouse="Đông Mát"><input type="checkbox" checked data-col="6" data-warehouse="Đông Mát" onchange="toggleColCheck(6,this)"> Rổ ABA đông mát</label>
<label class="dd-item" data-warehouse="Đông Mát"><input type="checkbox" checked data-col="7" data-warehouse="Đông Mát" onchange="toggleColCheck(7,this)"> Tote ABA đông mát</label>
<label class="dd-item" data-warehouse="Rau"><input type="checkbox" checked data-col="8" data-warehouse="Rau" onchange="toggleColCheck(8,this)"> Tote đỏ bánh tươi</label>
</div>
            </div>
        </div>
        <div class="filter-group">
            <span class="filter-label">Tìm kiếm</span>
            <div class="search-wrap">
                <input class="filter-select search-upper" type="text" id="store-search" placeholder="Mã ST hoặc tên..." oninput="this.value=this.value.toUpperCase();filterStore()">
                <button class="search-clear" onclick="clearSearch('store-search','filterStore')">&times;</button>
            </div>
        </div>
"""

        legend_html = """
        <div class="color-legend" style="margin-bottom: 0;">
            <span class="legend-title">Tồn kho:</span>
            <span class="legend-item"><span class="legend-dot ld-green"></span>&lt; 30</span>
            <span class="legend-item"><span class="legend-dot ld-yellow"></span>30 – 50</span>
            <span class="legend-item"><span class="legend-dot ld-orange"></span>50 – 60</span>
            <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 60</span>
        </div>
"""

        new_tonkho = f"""<div class="top-controls"{top_attrs}>
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
        <div class="stats-bar" style="width: 420px; flex-shrink: 0; justify-content: flex-start; gap: 8px; padding-left: 12px; margin-bottom: 0;">
            {stats_content}
        </div>
        <div style="flex: 1;"></div>
    </div>
"""
        idx_html = idx_html[:match_tk.start()] + new_tonkho + idx_html[match_tk.end():]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx_html)

if __name__ == '__main__':
    fix_layout()
