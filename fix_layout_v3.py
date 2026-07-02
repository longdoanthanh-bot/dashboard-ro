import re

def fix_tonkho_v3():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the Tồn Kho controls section
    pattern = re.compile(r'<div class="top-controls".*?<!-- Row 2: Stats Block on left -->.*?</div>\s*</div>\s*</div>', re.DOTALL)
    match = pattern.search(html)
    if not match:
        print("Tồn Kho top-controls not found!")
        return

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
        <button class="btn-export" onclick="exportTonKho()" style="align-self:flex-end;padding:6px 12px;font-size:11px;height:33px;margin-bottom:0;">📥 Tải Excel</button>
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

    stats_html = """
        <div class="stats-bar compact" style="justify-content: flex-start; gap: 12px; margin-bottom: 0;">
            <div class="stat blue"><div class="stat-num" id="tk-stat-st">197</div><div class="stat-label">Tổng ST có tồn</div></div>
            <div class="stat yellow"><div class="stat-num" id="tk-stat-total">25,487</div><div class="stat-label">Tổng rổ</div></div>
            <div class="stat green"><div class="stat-num" id="tk-stat-types">9</div><div class="stat-label">Loại rổ</div></div>
        </div>
    """

    new_tonkho = f"""<div class="top-controls" style="display: flex; flex-direction: column; align-items: stretch; justify-content: flex-start; padding-left: 420px; flex-wrap: nowrap; gap: 12px; margin-bottom: 12px; position: relative; z-index: 10;">
    <!-- Row 1: Filters + Excel -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end; width: 100%;">
        {filters_html}
    </div>

    <!-- Row 2: Stats Block + Legend -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end; width: 100%;">
        {stats_html}
        <div style="flex: 1;"></div>
        {legend_html}
    </div>
</div>"""

    html = html[:match.start()] + new_tonkho + html[match.end():]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    fix_tonkho_v3()
