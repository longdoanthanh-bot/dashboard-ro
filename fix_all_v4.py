import re

def fix_all_v4():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # --- 1. Tồn Kho ---
    # Left: Empty
    # Right R1: Filters + Excel
    # Right R2: Stats + Legend
    tk_filters = """
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
    tk_legend = """
        <div class="color-legend" style="margin-bottom: 0;">
            <span class="legend-title">Tồn kho:</span>
            <span class="legend-item"><span class="legend-dot ld-green"></span>&lt; 30</span>
            <span class="legend-item"><span class="legend-dot ld-yellow"></span>30 – 50</span>
            <span class="legend-item"><span class="legend-dot ld-orange"></span>50 – 60</span>
            <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 60</span>
        </div>
    """
    tk_stats = """
        <div class="stats-bar compact" style="justify-content: flex-start; gap: 12px; margin-bottom: 0;">
            <div class="stat blue"><div class="stat-num" id="tk-stat-st">197</div><div class="stat-label">Tổng ST có tồn</div></div>
            <div class="stat yellow"><div class="stat-num" id="tk-stat-total">25,487</div><div class="stat-label">Tổng rổ</div></div>
            <div class="stat green"><div class="stat-num" id="tk-stat-types">9</div><div class="stat-label">Loại rổ</div></div>
        </div>
    """
    tk_html = f"""<div class="top-controls" style="display: flex; flex-direction: row; gap: 12px; margin-bottom: 12px; align-items: flex-end; position: relative; z-index: 10;">
    <div style="width: 420px; flex-shrink: 0; display: flex; flex-direction: column; gap: 12px;">
        <div style="min-height: 70px;"></div>
    </div>
    <div style="flex: 1; display: flex; flex-direction: column; gap: 12px; justify-content: flex-end;">
        <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end;">
            {tk_filters}
        </div>
        <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end;">
            {tk_stats}
            <div style="flex: 1;"></div>
            {tk_legend}
        </div>
    </div>
</div>"""

    # --- 2. Thu Hồi ---
    # Left: Stats Block
    # Right R1: Filters + Excel
    # Right R2: Legend + Date Bar
    th_filters = """
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
    th_legend = """
        <div class="color-legend" style="margin-bottom: 0;">
            <span class="legend-title">Chênh lệch:</span>
            <span class="legend-item"><span class="legend-dot ld-green"></span>0 (đủ)</span>
            <span class="legend-item"><span class="legend-dot ld-yellow"></span>&lt; 10</span>
            <span class="legend-item"><span class="legend-dot ld-orange"></span>10 – 30</span>
            <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 30</span>
        </div>
    """
    th_date = """
        <div class="cal-bar" style="margin-bottom: 0;" id="trip-date-bar">
        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
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
    th_stats = """
        <div class="stats-bar" style="margin-bottom: 0;">
            <div class="stat red"><div class="stat-num">113</div><div class="stat-label">Lượt chưa thu</div></div>
            <div class="stat green"><div class="stat-num">865</div><div class="stat-label">Lượt đã thu</div></div>
            <div class="stat blue"><div class="stat-num">111,940</div><div class="stat-label">Tổng SL Giao</div></div>
            <div class="stat green"><div class="stat-num">109,262</div><div class="stat-label">Tổng SL Thu</div></div>
        </div>
    """
    th_html = f"""<div class="top-controls-thuhoi" id="thuhoi-controls" style="display: flex; flex-direction: row; gap: 12px; margin-bottom: 12px; align-items: flex-end; position: relative; z-index: 10;">
    <div style="width: 420px; flex-shrink: 0; display: flex; flex-direction: column; gap: 12px;">
        <div style="min-height: 70px;"></div>
        {th_stats}
    </div>
    <div style="flex: 1; display: flex; flex-direction: column; gap: 12px; justify-content: flex-end;">
        <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end;">
            {th_filters}
        </div>
        <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end;">
            {th_legend}
            <div style="flex: 1;"></div>
            {th_date}
        </div>
    </div>
</div>"""

    # --- 3. Sơ Đồ ---
    # Left: Empty
    # Right R1: Filters + Excel (if any)
    # Right R2: Stats + Legend
    # Let's extract existing Sơ Đồ top-controls to see what filters it has.
    map_pattern = re.compile(r'<div class="map-controls".*?<!-- MAP STATS MOVED TO LEFT -->.*?</div>\s*</div>\s*</div>', re.DOTALL)
    map_match = map_pattern.search(html)
    if map_match:
        map_filters = """
            <div class="filter-group">
                <span class="filter-label">Kho</span>
                <select class="filter-select" id="map-wh-filter" onchange="filterMapWarehouse(this.value)">
                    <option value="">Tất cả</option>
                    <option value="Khô">Khô</option>
                    <option value="Rau">Rau</option>
                    <option value="Đông Mát">Đông Mát</option>
                </select>
            </div>
            <div class="filter-group">
                <span class="filter-label">Tìm kiếm ST</span>
                <div class="search-wrap">
                    <input class="filter-select search-upper" type="text" id="map-store-search" placeholder="Nhập mã/tên ST..." oninput="this.value=this.value.toUpperCase();searchMapStore()">
                    <button class="search-clear" onclick="clearSearch('map-store-search','searchMapStore')">&times;</button>
                </div>
            </div>
            <button class="btn-export" onclick="resetMapZoom()" style="align-self:flex-end;padding:6px 12px;font-size:11px;height:33px;margin-bottom:0;">Mặc định</button>
        """
        map_stats = """
            <div class="map-stats compact" style="margin-bottom: 0;">
                <div class="stat blue"><div class="stat-num" id="map-total-st">0</div><div class="stat-label">Tổng ST hiển thị</div></div>
                <div class="stat yellow"><div class="stat-num" id="map-total-ro">0</div><div class="stat-label">Tổng rổ tồn</div></div>
            </div>
        """
        map_legend = """
            <div class="color-legend" style="margin-bottom: 0;">
                <span class="legend-title">Tồn kho:</span>
                <span class="legend-item"><span class="legend-dot ld-green"></span>&lt; 30</span>
                <span class="legend-item"><span class="legend-dot ld-yellow"></span>30 – 50</span>
                <span class="legend-item"><span class="legend-dot ld-orange"></span>50 – 60</span>
                <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 60</span>
            </div>
        """
        map_html = f"""<div class="map-controls" style="display: flex; flex-direction: row; gap: 12px; margin-bottom: 12px; align-items: flex-end; position: relative; z-index: 10;">
    <div style="width: 420px; flex-shrink: 0; display: flex; flex-direction: column; gap: 12px;">
        <div style="min-height: 70px;"></div>
    </div>
    <div style="flex: 1; display: flex; flex-direction: column; gap: 12px; justify-content: flex-end;">
        <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end;">
            {map_filters}
        </div>
        <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end;">
            {map_stats}
            <div style="flex: 1;"></div>
            {map_legend}
        </div>
    </div>
</div>"""

    # --- 4. Công Việc ---
    # Has a date bar as well!
    # Left: Stats Block
    # Right R1: Filters
    # Right R2: Date Bar
    task_pattern = re.compile(r'<div class="top-controls-tasks".*?<!-- TASKS STATS MOVED TO LEFT -->.*?</div>\s*</div>\s*</div>', re.DOTALL)
    task_match = task_pattern.search(html)
    if task_match:
        task_date = """
            <div class="cal-bar" style="margin-bottom: 0; flex: 1;" id="task-date-bar">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;flex-wrap:wrap;">
                <span class="cal-title">📅 Khoảng ngày</span>
                <div style="display:flex;gap:6px;align-items:center;">
                    <label style="color:var(--text3);font-size:10px;">Từ</label>
                    <input type="date" id="task-date-from" value="2026-06-26" onchange="filterTaskDate()" style="background:var(--bg3);border:1px solid var(--border);border-radius:5px;color:var(--text);padding:3px 6px;font-size:11px;font-family:inherit;">
                    <label style="color:var(--text3);font-size:10px;">Đến</label>
                    <input type="date" id="task-date-to" value="2026-07-02" onchange="filterTaskDate()" style="background:var(--bg3);border:1px solid var(--border);border-radius:5px;color:var(--text);padding:3px 6px;font-size:11px;font-family:inherit;">
                </div>
            </div>
            </div>
        """
        task_filters = """
            <div class="filter-group">
                <span class="filter-label">Loại CV</span>
                <select class="filter-select" id="task-type-filter" onchange="filterTasks()">
                    <option value="">Tất cả</option>
                    <option value="THU_HOI">Thu hồi</option>
                    <option value="KIEM_KE">Kiểm kê</option>
                    <option value="XU_LY_CHENH_LECH">Xử lý chênh lệch</option>
                </select>
            </div>
            <div class="filter-group">
                <span class="filter-label">Trạng thái</span>
                <select class="filter-select" id="task-status-filter" onchange="filterTasks()">
                    <option value="">Tất cả</option>
                    <option value="TODO">Cần làm</option>
                    <option value="IN_PROGRESS">Đang làm</option>
                    <option value="DONE">Hoàn thành</option>
                </select>
            </div>
        """
        task_stats = """
            <div class="stats-bar" style="margin-bottom: 0;">
                <div class="stat yellow"><div class="stat-num" id="task-stat-todo">0</div><div class="stat-label">Cần làm</div></div>
                <div class="stat blue"><div class="stat-num" id="task-stat-prog">0</div><div class="stat-label">Đang làm</div></div>
                <div class="stat green"><div class="stat-num" id="task-stat-done">0</div><div class="stat-label">Hoàn thành</div></div>
            </div>
        """
        task_html = f"""<div class="top-controls-tasks" id="task-controls" style="display: flex; flex-direction: row; gap: 12px; margin-bottom: 12px; align-items: flex-end; position: relative; z-index: 10;">
    <div style="width: 420px; flex-shrink: 0; display: flex; flex-direction: column; gap: 12px;">
        <div style="min-height: 70px;"></div>
        {task_stats}
    </div>
    <div style="flex: 1; display: flex; flex-direction: column; gap: 12px; justify-content: flex-end;">
        <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end;">
            {task_filters}
            <div style="flex: 1;"></div>
            <button class="btn-export" onclick="openAddTaskModal()" style="padding:6px 12px;font-size:11px;height:33px;margin-bottom:0;">+ Thêm CV</button>
        </div>
        <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end;">
            {task_date}
        </div>
    </div>
</div>"""

    # Apply all changes
    # Re-read to apply sequentially
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Apply Tồn Kho
    tk_pat = re.compile(r'<div class="top-controls" style="display: flex; flex-direction: column; align-items: stretch; justify-content: flex-start; padding-left: 420px;.*?>.*?</div>\s*</div>\s*</div>', re.DOTALL)
    if tk_pat.search(html):
        html = html[:tk_pat.search(html).start()] + tk_html + html[tk_pat.search(html).end():]
    else:
        # try old pattern if v3 wasn't applied
        tk_pat_old = re.compile(r'<div class="top-controls".*?<!-- Row 2: Stats Block on left -->.*?</div>\s*</div>\s*</div>', re.DOTALL)
        if tk_pat_old.search(html):
            html = html[:tk_pat_old.search(html).start()] + tk_html + html[tk_pat_old.search(html).end():]

    # Apply Thu Hồi
    th_pat = re.compile(r'<div class="top-controls-thuhoi" id="thuhoi-controls".*?<!-- Row 3: Stats Block .*?</div>\s*</div>\s*</div>', re.DOTALL)
    if th_pat.search(html):
        html = html[:th_pat.search(html).start()] + th_html + html[th_pat.search(html).end():]

    # Apply Sơ Đồ
    if map_match:
        html = html[:map_pattern.search(html).start()] + map_html + html[map_pattern.search(html).end():]

    # Apply Công Việc
    if task_match:
        html = html[:task_pattern.search(html).start()] + task_html + html[task_pattern.search(html).end():]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    fix_all_v4()
