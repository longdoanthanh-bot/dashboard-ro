import re

def fix_th_v3():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    pattern = re.compile(r'<div class="top-controls-thuhoi" id="thuhoi-controls".*?<!-- Row 3: Stats Block on left -->.*?</div>\s*</div>\s*</div>', re.DOTALL)
    match = pattern.search(html)
    if not match:
        print("Thu Hồi controls not found!")
        return

    cal_bar_html = """
        <div class="cal-bar" style="margin-bottom: 0; flex: 1;" id="trip-date-bar">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;flex-wrap:wrap;">
            <span class="cal-title">📅 Khoảng ngày</span>
            <div style="display:flex;gap:6px;align-items:center;">
                <label style="color:var(--text3);font-size:10px;">Từ</label>
                <input type="date" id="date-from" value="2026-06-26" min="2026-06-26" max="2026-07-02" onchange="filterDateRange()" style="background:var(--bg3);border:1px solid var(--border);border-radius:5px;color:var(--text);padding:3px 6px;font-size:11px;font-family:inherit;">
                <label style="color:var(--text3);font-size:10px;">Đến</label>
                <input type="date" id="date-to" value="2026-07-02" min="2026-06-26" max="2026-07-02" onchange="filterDateRange()" style="background:var(--bg3);border:1px solid var(--border);border-radius:5px;color:var(--text);padding:3px 6px;font-size:11px;font-family:inherit;">
            </div>
            <div class="cal-grid">
<!-- CAL_GRID_START -->
<div class="cal-day" onclick="toggleDate('26/06/2026',this)" data-date="26/06/2026" data-iso="2026-06-26"><div class="cal-date">26</div><div class="cal-badge"><span class="badge-nr">0</span> chưa</div></div>
<div class="cal-day" onclick="toggleDate('27/06/2026',this)" data-date="27/06/2026" data-iso="2026-06-27"><div class="cal-date">27</div><div class="cal-badge"><span class="badge-nr">0</span> chưa</div></div>
<div class="cal-day" onclick="toggleDate('28/06/2026',this)" data-date="28/06/2026" data-iso="2026-06-28"><div class="cal-date">28</div><div class="cal-badge"><span class="badge-nr">157</span> chưa</div></div>
<div class="cal-day" onclick="toggleDate('29/06/2026',this)" data-date="29/06/2026" data-iso="2026-06-29"><div class="cal-date">29</div><div class="cal-badge"><span class="badge-nr">38</span> chưa</div></div>
<div class="cal-day" onclick="toggleDate('30/06/2026',this)" data-date="30/06/2026" data-iso="2026-06-30"><div class="cal-date">30</div><div class="cal-badge"><span class="badge-nr">77</span> chưa</div></div>
<div class="cal-day" onclick="toggleDate('01/07/2026',this)" data-date="01/07/2026" data-iso="2026-07-01"><div class="cal-date">01</div><div class="cal-badge"><span class="badge-nr">102</span> chưa</div></div>
<div class="cal-day active" onclick="toggleDate('02/07/2026',this)" data-date="02/07/2026" data-iso="2026-07-02"><div class="cal-date">02</div><div class="cal-badge"><span class="badge-nr">160</span> chưa</div></div>
<!-- CAL_GRID_END -->
            </div>
        </div>
        </div>
    """

    filters_html = """
        <div class="filter-group">
            <span class="filter-label">Kho</span>
            <select class="filter-select" id="trip-wh-filter" onchange="filterTripWarehouse(this.value)">
                <option value="">Tất cả</option>
<option value="Khô">Khô</option>
<option value="Rau">Rau</option>
<option value="Đông Mát">Đông Mát</option>

            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">Trạng thái</span>
            <div class="dropdown-wrap" id="status-filter">
                <button class="filter-select dropdown-btn" type="button" onclick="toggleDD('status-dd')">Tất cả</button>
                <div class="dropdown-panel" id="status-dd">
                    <label class="dd-item"><input type="checkbox" checked onchange="toggleStatusCheck(null,this)"> Tất cả</label>
                    <label class="dd-item"><input type="checkbox" checked data-status="none" onchange="toggleStatusCheck('none',this)"> ✗ Không thu</label>
                    <label class="dd-item"><input type="checkbox" checked data-status="partial" onchange="toggleStatusCheck('partial',this)"> ⚠ Thu 1 phần</label>
                    <label class="dd-item"><input type="checkbox" checked data-status="full" onchange="toggleStatusCheck('full',this)"> ✓ Đã thu hết</label>
                </div>
            </div>
        </div>
        <div class="filter-group">
            <span class="filter-label">Hiển thị</span>
            <select class="filter-select" onchange="filterTopTrip(+this.value)">
                <option value="10">Top 10</option><option value="20">Top 20</option>
                <option value="50">Top 50</option><option value="9999" selected>Tất cả</option>
            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">Loại rổ</span>
            <div class="dropdown-wrap" id="basket-filter">
                <button class="filter-select dropdown-btn" type="button" onclick="toggleDD('basket-dd')">Tất cả</button>
                <div class="dropdown-panel" id="basket-dd"><label class="dd-item"><input type="checkbox" checked onchange="toggleBasketCheck(null,this)"> Tất cả</label>
<label class="dd-item" data-warehouse="Khô"><input type="checkbox" checked data-basket="B0001" data-warehouse="Khô" onchange="toggleBasketCheck('B0001',this)">Seedlog - Thùng tote xanh</label>
<label class="dd-item" data-warehouse=""><input type="checkbox" checked data-basket="B0002" data-warehouse="" onchange="toggleBasketCheck('B0002',this)">Thùng Carton, Bịch nguyên</label>
<label class="dd-item" data-warehouse="Rau"><input type="checkbox" checked data-basket="B0012" data-warehouse="Rau" onchange="toggleBasketCheck('B0012',this)">KRC Rổ nhựa đen xếp chồng</label>
<label class="dd-item" data-warehouse="Đông Mát"><input type="checkbox" checked data-basket="B0015" data-warehouse="Đông Mát" onchange="toggleBasketCheck('B0015',this)">Rổ ABA đông mát</label>
<label class="dd-item" data-warehouse="Đông Mát"><input type="checkbox" checked data-basket="B0016" data-warehouse="Đông Mát" onchange="toggleBasketCheck('B0016',this)">Tote ABA đông mát</label>
<label class="dd-item" data-warehouse="Rau"><input type="checkbox" checked data-basket="B0017" data-warehouse="Rau" onchange="toggleBasketCheck('B0017',this)">Tote đỏ bánh tươi</label>
</div>
            </div>
        </div>
        <div class="filter-group">
            <span class="filter-label">Tìm kiếm</span>
            <div class="search-wrap">
                <input class="filter-select search-upper" type="text" id="trip-store-search" placeholder="Mã ST hoặc tên..." oninput="this.value=this.value.toUpperCase();filterTripStore()">
                <button class="search-clear" onclick="clearSearch('trip-store-search','filterTripStore')">&times;</button>
            </div>
        </div>
        <button class="btn-export" onclick="exportThuHoi()" style="align-self:flex-end;padding:6px 12px;font-size:11px;height:33px;margin-bottom:0;">📥 Tải Excel</button>
    """

    legend_html = """
        <div class="color-legend" style="margin-bottom: 0;">
            <span class="legend-title">Chênh lệch:</span>
            <span class="legend-item"><span class="legend-dot ld-green"></span>0 (đủ)</span>
            <span class="legend-item"><span class="legend-dot ld-yellow"></span>&lt; 10</span>
            <span class="legend-item"><span class="legend-dot ld-orange"></span>10 – 30</span>
            <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 30</span>
        </div>
    """

    stats_html = """
        <div class="stats-bar compact" style="justify-content: flex-start; gap: 12px; margin-bottom: 0;">
            <div class="stat red"><div class="stat-num">113</div><div class="stat-label">Lượt chưa thu</div></div>
            <div class="stat green"><div class="stat-num">865</div><div class="stat-label">Lượt đã thu</div></div>
            <div class="stat blue"><div class="stat-num">111,940</div><div class="stat-label">Tổng SL Giao</div></div>
            <div class="stat green"><div class="stat-num">109,262</div><div class="stat-label">Tổng SL Thu</div></div>
        </div>
    """

    new_thuhoi = f"""<div class="top-controls-thuhoi" id="thuhoi-controls" style="display: flex; flex-direction: column; align-items: stretch; justify-content: flex-start; padding-left: 420px; flex-wrap: nowrap; gap: 12px; margin-bottom: 12px; position: relative; z-index: 10;">
    <!-- Row 1: Date Bar -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-start; width: 100%;">
        {cal_bar_html}
    </div>
    
    <!-- Row 2: Filters + Excel -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end; width: 100%;">
        {filters_html}
    </div>

    <!-- Row 3: Stats Block + Legend -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end; width: 100%;">
        {stats_html}
        <div style="flex: 1;"></div>
        {legend_html}
    </div>
</div>"""

    html = html[:match.start()] + new_thuhoi + html[match.end():]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    fix_th_v3()
