def fix_left_stats():
    # ----- INDEX.HTML -----
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_html = f.read()

    # 1. Ensure .main-panel is relative
    if 'position:relative;' not in idx_html and '.main-panel { display:none; padding-top:16px; animation:fadeIn .3s; }' in idx_html:
        idx_html = idx_html.replace('.main-panel { display:none; padding-top:16px; animation:fadeIn .3s; }', 
                                    '.main-panel { display:none; padding-top:16px; animation:fadeIn .3s; position: relative; }')

    # 2. Tồn Kho
    old_tk_legend_stats = """    <div style="display: flex; flex-direction: row; align-items: center; gap: 12px; flex-wrap: nowrap; width: 100%;">
        <div class="color-legend">
            <span class="legend-title">Tồn kho:</span>
            <span class="legend-item"><span class="legend-dot ld-green"></span>&lt; 30</span>
            <span class="legend-item"><span class="legend-dot ld-yellow"></span>30 – 50</span>
            <span class="legend-item"><span class="legend-dot ld-orange"></span>50 – 60</span>
            <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 60</span>
        </div>
        <div class="stats-bar" style="margin-bottom: 0; padding-left: 10px;">
            <div class="stat blue"><div class="stat-num" id="tk-stat-st">197</div><div class="stat-label">Tổng ST có tồn</div></div>
            <div class="stat yellow"><div class="stat-num" id="tk-stat-total">25,487</div><div class="stat-label">Tổng rổ</div></div>
            <div class="stat green"><div class="stat-num" id="tk-stat-types">9</div><div class="stat-label">Loại rổ</div></div>
            <button class="btn-export" onclick="exportTonKho()">📥 Tải Excel</button>
        </div>
    </div>
    </div>"""

    new_tk_legend_stats = """    <div style="display: flex; flex-direction: row; align-items: center; gap: 12px; flex-wrap: nowrap; width: 100%;">
        <div class="color-legend">
            <span class="legend-title">Tồn kho:</span>
            <span class="legend-item"><span class="legend-dot ld-green"></span>&lt; 30</span>
            <span class="legend-item"><span class="legend-dot ld-yellow"></span>30 – 50</span>
            <span class="legend-item"><span class="legend-dot ld-orange"></span>50 – 60</span>
            <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 60</span>
        </div>
    </div>
    </div>
    <!-- STATS MOVED TO LEFT -->
    <div class="stats-bar" style="position: absolute; left: 12px; top: 110px; width: 380px; z-index: 20; padding-left: 0; justify-content: flex-start; gap: 8px;">
        <div class="stat blue"><div class="stat-num" id="tk-stat-st">197</div><div class="stat-label">Tổng ST có tồn</div></div>
        <div class="stat yellow"><div class="stat-num" id="tk-stat-total">25,487</div><div class="stat-label">Tổng rổ</div></div>
        <div class="stat green"><div class="stat-num" id="tk-stat-types">9</div><div class="stat-label">Loại rổ</div></div>
        <button class="btn-export" onclick="exportTonKho()">📥 Tải Excel</button>
    </div>"""
    
    idx_html = idx_html.replace(old_tk_legend_stats, new_tk_legend_stats)

    # 3. Thu Hồi
    old_th_legend_stats = """    <div style="display: flex; flex-direction: row; align-items: center; gap: 12px; flex-wrap: nowrap; width: 100%;">
        <div class="color-legend" style="margin-bottom: 0;">
            <span class="legend-title">Chênh lệch:</span>
            <span class="legend-item"><span class="legend-dot ld-green"></span>0 (đủ)</span>
            <span class="legend-item"><span class="legend-dot ld-yellow"></span>&lt; 10</span>
            <span class="legend-item"><span class="legend-dot ld-orange"></span>10 – 30</span>
            <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 30</span>
        </div>
        <div class="stats-bar compact" style="margin-bottom: 0; padding-left: 10px;">
            <div class="stat red"><div class="stat-num">113</div><div class="stat-label">Lượt chưa thu</div></div>
            <div class="stat green"><div class="stat-num">865</div><div class="stat-label">Lượt đã thu</div></div>
            <div class="stat blue"><div class="stat-num">111,940</div><div class="stat-label">Tổng SL Giao</div></div>
            <div class="stat green"><div class="stat-num">109,262</div><div class="stat-label">Tổng SL Thu</div></div>
            <button class="btn-export" onclick="exportThuHoi()" style="align-self:center;padding:5px 12px;font-size:11px;">📥 Excel</button>
        </div>
    </div>
    </div>"""

    new_th_legend_stats = """    <div style="display: flex; flex-direction: row; align-items: center; gap: 12px; flex-wrap: nowrap; width: 100%;">
        <div class="color-legend" style="margin-bottom: 0;">
            <span class="legend-title">Chênh lệch:</span>
            <span class="legend-item"><span class="legend-dot ld-green"></span>0 (đủ)</span>
            <span class="legend-item"><span class="legend-dot ld-yellow"></span>&lt; 10</span>
            <span class="legend-item"><span class="legend-dot ld-orange"></span>10 – 30</span>
            <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 30</span>
        </div>
    </div>
    </div>
    <!-- STATS MOVED TO LEFT -->
    <div class="stats-bar compact" style="position: absolute; left: 12px; top: 110px; width: 380px; z-index: 20; padding-left: 0; justify-content: flex-start; gap: 8px;">
        <div class="stat red"><div class="stat-num">113</div><div class="stat-label">Lượt chưa thu</div></div>
        <div class="stat green"><div class="stat-num">865</div><div class="stat-label">Lượt đã thu</div></div>
        <div class="stat blue"><div class="stat-num">111,940</div><div class="stat-label">Tổng SL Giao</div></div>
        <div class="stat green"><div class="stat-num">109,262</div><div class="stat-label">Tổng SL Thu</div></div>
        <button class="btn-export" onclick="exportThuHoi()" style="align-self:center;padding:5px 12px;font-size:11px;">📥 Excel</button>
    </div>"""

    idx_html = idx_html.replace(old_th_legend_stats, new_th_legend_stats)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx_html)


    # ----- TASKS.HTML -----
    with open('tasks.html', 'r', encoding='utf-8') as f:
        tsk_html = f.read()

    # In tasks.html, we have .top-row, which contains .add-form and .stats-row
    
    old_stats_row = """        <!-- STATS — LEFT SIDE (Now Bottom) -->
        <div class="stats-row" style="justify-content: flex-end;">
            <div class="stat-total-card" id="stat-total-card">
                <div class="stat-num" id="stat-total">0</div>
                <div class="stat-label">Tổng</div>
                <div class="stat-pct" id="stat-pct">0%</div>
            </div>
            <div class="stat-right-group">
                <div class="stat-card s-todo"><div class="stat-num" id="stat-todo">0</div><div class="stat-label">Chưa làm</div><div class="stat-pct-detail" id="pct-todo">0%</div></div>
                <div class="stat-card s-doing"><div class="stat-num" id="stat-doing">0</div><div class="stat-label">Đang làm</div><div class="stat-pct-detail" id="pct-doing">0%</div></div>
                <div class="stat-card s-done"><div class="stat-num" id="stat-done">0</div><div class="stat-label">Hoàn thành</div><div class="stat-pct-detail" id="pct-done">0%</div></div>
            </div>
        </div>
    </div>"""

    new_stats_row = """    </div>
        <!-- STATS — LEFT SIDE (Absolute Positioned under Giao dien) -->
        <div class="stats-row" style="position: absolute; left: 12px; top: 110px; width: 380px; z-index: 20; justify-content: flex-start; padding-left: 0;">
            <div class="stat-total-card" id="stat-total-card">
                <div class="stat-num" id="stat-total">0</div>
                <div class="stat-label">Tổng</div>
                <div class="stat-pct" id="stat-pct">0%</div>
            </div>
            <div class="stat-right-group">
                <div class="stat-card s-todo"><div class="stat-num" id="stat-todo">0</div><div class="stat-label">Chưa làm</div><div class="stat-pct-detail" id="pct-todo">0%</div></div>
                <div class="stat-card s-doing"><div class="stat-num" id="stat-doing">0</div><div class="stat-label">Đang làm</div><div class="stat-pct-detail" id="pct-doing">0%</div></div>
                <div class="stat-card s-done"><div class="stat-num" id="stat-done">0</div><div class="stat-label">Hoàn thành</div><div class="stat-pct-detail" id="pct-done">0%</div></div>
            </div>
        </div>"""

    tsk_html = tsk_html.replace(old_stats_row, new_stats_row)

    with open('tasks.html', 'w', encoding='utf-8') as f:
        f.write(tsk_html)

if __name__ == '__main__':
    fix_left_stats()
