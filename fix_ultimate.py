import re

def fix_ultimate():
    def build_layout(id_attr, class_attr, left_stats, right_rows):
        # right_rows is a list of strings, each is a row in the right column
        right_html = ""
        for row in right_rows:
            right_html += f"""
        <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: wrap; align-items: flex-end; width: 100%;">
            {row}
        </div>"""
        
        return f"""<div class="{class_attr}" {id_attr} style="display: flex; flex-direction: row; gap: 12px; margin-bottom: 12px; align-items: flex-start; position: relative; z-index: 10; width: 100%;">
    <!-- LEFT COLUMN -->
    <div style="width: 420px; flex-shrink: 0; display: flex; flex-direction: column; gap: 12px;">
        <div style="min-height: 70px;"></div>
        {left_stats}
    </div>
    <!-- RIGHT COLUMN -->
    <div style="flex: 1; display: flex; flex-direction: column; gap: 12px; min-width: 0;">
        {right_html}
    </div>
</div>"""

    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # --- 1. Tồn Kho ---
    tk_stats = """
        <div class="stats-bar compact" style="justify-content: flex-start; margin-bottom: 0; background: var(--bg2); padding: 8px; border-radius: 8px; border: 1px solid var(--border);">
            <div class="stat blue" style="flex:1;"><div class="stat-num" id="tk-stat-st">197</div><div class="stat-label">Tổng ST có tồn</div></div>
            <div class="stat yellow" style="flex:1;"><div class="stat-num" id="tk-stat-total">25,487</div><div class="stat-label">Tổng rổ</div></div>
            <div class="stat green" style="flex:1;"><div class="stat-num" id="tk-stat-types">9</div><div class="stat-label">Loại rổ</div></div>
        </div>
    """
    tk_row1 = """
            <div class="filter-group">
                <span class="filter-label">Kho</span>
                <select class="filter-select" id="tonkho-wh-filter" onchange="filterWarehouse(this.value)">
                    <option value="">Tất cả</option><option value="Khô">Khô</option><option value="Rau">Rau</option><option value="Đông Mát">Đông Mát</option>
                </select>
            </div>
            <div class="filter-group">
                <span class="filter-label">Hiển thị</span>
                <select class="filter-select" id="tonkho-top-filter" onchange="filterTop(+this.value)">
                    <option value="10">Top 10</option><option value="20">Top 20</option><option value="50">Top 50</option><option value="100">Top 100</option><option value="9999" selected>Tất cả</option>
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
<label class="dd-item" data-warehouse="Rau"><input type="checkbox" checked data-col="8" data-warehouse="Rau" onchange="toggleColCheck(8,this)"> Tote đỏ bánh tươi</label></div>
                </div>
            </div>
            <div class="filter-group">
                <span class="filter-label">Tìm kiếm</span>
                <div class="search-wrap">
                    <input class="filter-select search-upper" type="text" id="store-search" placeholder="Mã ST hoặc tên..." oninput="this.value=this.value.toUpperCase();filterStore()">
                    <button class="search-clear" onclick="clearSearch('store-search','filterStore')">&times;</button>
                </div>
            </div>
            <div style="flex: 1;"></div>
            <button class="btn-export" onclick="exportTonKho()" style="padding:6px 12px;font-size:11px;height:33px;margin-bottom:0;">📥 Tải Excel</button>
    """
    tk_row2 = """
            <div class="color-legend" style="margin-bottom: 0;">
                <span class="legend-title">Tồn kho:</span>
                <span class="legend-item"><span class="legend-dot ld-green"></span>&lt; 30</span>
                <span class="legend-item"><span class="legend-dot ld-yellow"></span>30 – 50</span>
                <span class="legend-item"><span class="legend-dot ld-orange"></span>50 – 60</span>
                <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 60</span>
            </div>
    """
    tk_html = build_layout('', 'top-controls', tk_stats, [tk_row1, tk_row2])

    # --- 2. Thu Hồi ---
    th_stats = """
        <div class="stats-bar compact" style="justify-content: flex-start; margin-bottom: 0; background: var(--bg2); padding: 8px; border-radius: 8px; border: 1px solid var(--border);">
            <div class="stat red" style="flex:1;"><div class="stat-num">113</div><div class="stat-label">Lượt chưa thu</div></div>
            <div class="stat green" style="flex:1;"><div class="stat-num">865</div><div class="stat-label">Lượt đã thu</div></div>
            <div class="stat blue" style="flex:1;"><div class="stat-num">111,940</div><div class="stat-label">Tổng SL Giao</div></div>
            <div class="stat green" style="flex:1;"><div class="stat-num">109,262</div><div class="stat-label">Tổng SL Thu</div></div>
        </div>
    """
    th_row1 = """
            <div class="filter-group">
                <span class="filter-label">Kho</span>
                <select class="filter-select" id="trip-wh-filter" onchange="filterTripWarehouse(this.value)">
                    <option value="">Tất cả</option><option value="Khô">Khô</option><option value="Rau">Rau</option><option value="Đông Mát">Đông Mát</option>
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
                    <option value="10">Top 10</option><option value="20">Top 20</option><option value="50">Top 50</option><option value="9999" selected>Tất cả</option>
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
<label class="dd-item" data-warehouse="Rau"><input type="checkbox" checked data-basket="B0017" data-warehouse="Rau" onchange="toggleBasketCheck('B0017',this)">Tote đỏ bánh tươi</label></div>
                </div>
            </div>
            <div class="filter-group">
                <span class="filter-label">Tìm kiếm</span>
                <div class="search-wrap">
                    <input class="filter-select search-upper" type="text" id="trip-store-search" placeholder="Mã ST hoặc tên..." oninput="this.value=this.value.toUpperCase();filterTripStore()">
                    <button class="search-clear" onclick="clearSearch('trip-store-search','filterTripStore')">&times;</button>
                </div>
            </div>
            <div style="flex: 1;"></div>
            <button class="btn-export" onclick="exportThuHoi()" style="padding:6px 12px;font-size:11px;height:33px;margin-bottom:0;">📥 Tải Excel</button>
    """
    th_row2 = """
            <div class="color-legend" style="margin-bottom: 0;">
                <span class="legend-title">Chênh lệch:</span>
                <span class="legend-item"><span class="legend-dot ld-green"></span>0 (đủ)</span>
                <span class="legend-item"><span class="legend-dot ld-yellow"></span>&lt; 10</span>
                <span class="legend-item"><span class="legend-dot ld-orange"></span>10 – 30</span>
                <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 30</span>
            </div>
            <div style="flex: 1;"></div>
            <div class="cal-bar" style="margin-bottom: 0; min-width: 0;" id="trip-date-bar">
                <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                    <span class="cal-title" style="white-space:nowrap;">📅 Khoảng ngày</span>
                    <div style="display:flex;gap:6px;align-items:center;">
                        <label style="color:var(--text3);font-size:10px;">Từ</label>
                        <input type="date" id="date-from" value="2026-06-26" min="2026-06-26" max="2026-07-02" onchange="filterDateRange()" style="background:var(--bg3);border:1px solid var(--border);border-radius:5px;color:var(--text);padding:3px 6px;font-size:11px;font-family:inherit;width:110px;">
                        <label style="color:var(--text3);font-size:10px;">Đến</label>
                        <input type="date" id="date-to" value="2026-07-02" min="2026-06-26" max="2026-07-02" onchange="filterDateRange()" style="background:var(--bg3);border:1px solid var(--border);border-radius:5px;color:var(--text);padding:3px 6px;font-size:11px;font-family:inherit;width:110px;">
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
    th_html = build_layout('id="thuhoi-controls"', 'top-controls-thuhoi', th_stats, [th_row1, th_row2])

    # --- 3. Sơ Đồ ---
    map_stats = """
        <div class="stats-bar compact" style="justify-content: flex-start; margin-bottom: 0; background: var(--bg2); padding: 8px; border-radius: 8px; border: 1px solid var(--border);">
            <div class="stat blue" style="flex:1;"><div class="stat-num" id="map-total-st">300</div><div class="stat-label">Tổng ST hiển thị</div></div>
            <div class="stat yellow" style="flex:1;"><div class="stat-num" id="map-total-mart">28</div><div class="stat-label">Mart</div></div>
            <div class="stat green" style="flex:1;"><div class="stat-num" id="map-total-mini">272</div><div class="stat-label">Mini</div></div>
        </div>
    """
    map_row1 = """
            <div class="filter-group">
                <span class="filter-label">Location Type</span>
                <select class="filter-select" id="map-loc-filter" onchange="filterMapStore()">
                    <option value="">Tất cả</option><option value="Mart">Mart</option><option value="Mini">Mini</option>
                </select>
            </div>
            <div class="filter-group">
                <span class="filter-label">Doanh thu</span>
                <select class="filter-select" id="map-rev-filter" onchange="filterMapStore()">
                    <option value="">Tất cả</option><option value="A">Mức A (>4B)</option><option value="B">Mức B (2-4B)</option><option value="C">Mức C (<2B)</option>
                </select>
            </div>
            <div class="filter-group">
                <span class="filter-label">Tìm kiếm ST</span>
                <div class="search-wrap">
                    <input class="filter-select search-upper" type="text" id="map-store-search" placeholder="Gõ mã ST, Enter..." oninput="this.value=this.value.toUpperCase();">
                    <button class="search-clear" onclick="clearSearch('map-store-search','searchMapStore')">&times;</button>
                </div>
            </div>
            <div class="filter-group">
                <span class="filter-label">Lân cận</span>
                <select class="filter-select" id="map-nearby-filter" onchange="filterMapStore()">
                    <option value="3">Top 3</option><option value="5" selected>Top 5</option><option value="10">Top 10</option>
                </select>
            </div>
            <div style="flex: 1;"></div>
            <button class="btn-export" onclick="resetMapZoom()" style="padding:6px 12px;font-size:11px;height:33px;margin-bottom:0;">📥 Xuất Excel</button>
    """
    map_row2 = """
            <div class="filter-group">
                <span class="filter-label">Đo KC: Điểm A</span>
                <input class="filter-select search-upper" type="text" id="dist-a" placeholder="GÕ MÃ ST...">
            </div>
            <div class="filter-group">
                <span class="filter-label">Điểm B</span>
                <input class="filter-select search-upper" type="text" id="dist-b" placeholder="GÕ MÃ ST...">
            </div>
            <button class="btn-export" onclick="calcDistance()" style="padding:6px 12px;font-size:11px;height:33px;margin-bottom:0;">📏 Tính KC</button>
            <div style="flex: 1;"></div>
            <div class="color-legend" style="margin-bottom: 0;">
                <span class="legend-title">DOANH THU:</span>
                <span class="legend-item"><span class="legend-dot ld-green"></span>A (>4B)</span>
                <span class="legend-item"><span class="legend-dot ld-blue"></span>B (2-4B)</span>
                <span class="legend-item"><span class="legend-dot" style="background:#757575;"></span>C (<2B)</span>
                <span class="legend-title" style="margin-left:8px;">LOẠI:</span>
                <span class="legend-item"><span class="legend-dot ld-orange"></span>Mart</span>
                <span class="legend-item"><span class="legend-dot" style="background:#9c27b0;"></span>Mini</span>
            </div>
    """
    map_html = build_layout('', 'map-controls', map_stats, [map_row1, map_row2])

    # Replace in index.html
    tk_pat = re.compile(r'<div class="top-controls"[^>]*>.*?</div>\s*</div>\s*</div>', re.DOTALL)
    if tk_pat.search(html):
        html = html[:tk_pat.search(html).start()] + tk_html + html[tk_pat.search(html).end():]

    th_pat = re.compile(r'<div class="top-controls-thuhoi" id="thuhoi-controls"[^>]*>.*?</div>\s*</div>\s*</div>', re.DOTALL)
    if th_pat.search(html):
        html = html[:th_pat.search(html).start()] + th_html + html[th_pat.search(html).end():]

    map_pat = re.compile(r'<div class="map-controls"[^>]*>.*?</div>\s*</div>\s*</div>', re.DOTALL)
    if map_pat.search(html):
        html = html[:map_pat.search(html).start()] + map_html + html[map_pat.search(html).end():]
        
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    # --- tasks.html ---
    with open('tasks.html', 'r', encoding='utf-8') as f:
        tasks_html = f.read()
        
    # First we need to extract the "Thêm task mới" (.add-form) div from tasks.html so we can put it in our layout!
    # Wait, the add-form has ID 'task-form'. Let's extract it.
    add_form_match = re.search(r'<div class="add-form" id="task-form".*?</form>\s*</div>', tasks_html, re.DOTALL)
    if not add_form_match:
        print("tasks.html add-form not found!")
        return
        
    add_form_html = add_form_match.group(0)
    
    tasks_stats = """
        <div class="stats-bar compact" style="justify-content: flex-start; margin-bottom: 0; background: var(--bg2); padding: 8px; border-radius: 8px; border: 1px solid var(--border);">
            <div class="stat green" style="flex:1;"><div class="stat-num">30</div><div class="stat-label">TỔNG <span style="font-size:8px;">90%</span></div></div>
            <div class="stat" style="flex:1;background:rgba(255,167,38,0.1);"><div class="stat-num" style="color:#ffa726;">1</div><div class="stat-label">CHƯA LÀM <span style="font-size:8px;">3%</span></div></div>
            <div class="stat" style="flex:1;background:rgba(41,182,246,0.1);"><div class="stat-num" style="color:#29b6f6;">2</div><div class="stat-label">ĐANG LÀM <span style="font-size:8px;">7%</span></div></div>
            <div class="stat" style="flex:1;background:rgba(102,187,106,0.1);"><div class="stat-num" style="color:#66bb6a;">27</div><div class="stat-label">HOÀN THÀNH <span style="font-size:8px;">90%</span></div></div>
        </div>
    """
    # Replace the existing top-row or whatever it is in tasks.html
    # In tasks.html, it's `<div class="top-row">...</div>`
    top_row_match = re.search(r'<div class="top-row">.*?</div>\s*</div>', tasks_html, re.DOTALL)
    if not top_row_match:
        print("tasks.html top-row not found!")
        return
        
    # I will replace `<div class="top-row">...</div>` and the `add_form` completely with the new structure.
    # Actually, let's just re-build the whole top section up to `<div class="board">`.
    # Wait, in tasks.html, `<div class="main-content">` contains `<div class="top-row">`, then `<div class="add-form">`, then `<div class="board">`.
    # I will replace everything between `<div class="main-content">` and `<div class="board">`.
    main_pattern = re.compile(r'(<div class="main-content">).*?(<div class="board">)', re.DOTALL)
    
    # We will build a unified top section for tasks.html
    tasks_top = f"""<div class="main-content">
    <div style="display: flex; flex-direction: row; gap: 12px; margin-bottom: 12px; align-items: flex-start; position: relative; z-index: 10; width: 100%;">
        <!-- LEFT COLUMN: Stats -->
        <div style="width: 420px; flex-shrink: 0; display: flex; flex-direction: column; gap: 12px;">
            <div style="min-height: 70px;"></div>
            {tasks_stats}
        </div>
        <!-- RIGHT COLUMN: Add Form -->
        <div style="flex: 1; display: flex; flex-direction: column; gap: 12px; min-width: 0;">
            {add_form_html}
        </div>
    </div>
"""
    
    if main_pattern.search(tasks_html):
        tasks_html = tasks_html[:main_pattern.search(tasks_html).start(1)] + tasks_top + tasks_html[main_pattern.search(tasks_html).start(2):]
        with open('tasks.html', 'w', encoding='utf-8') as f:
            f.write(tasks_html)
    else:
        print("tasks.html board not found!")
        
if __name__ == '__main__':
    fix_ultimate()
