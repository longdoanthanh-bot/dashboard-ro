import re

def fix_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Tồn kho
    old_top_ctrl_tk = '<div class="top-controls" style="display: flex; flex-direction: row; align-items: flex-start; justify-content: flex-start; padding-left: 420px; flex-wrap: wrap; gap: 12px; margin-bottom: 12px; min-height: 80px; position: relative; z-index: 10;">'
    new_top_ctrl_tk = '<div class="top-controls" style="display: flex; flex-direction: column; align-items: stretch; justify-content: flex-start; padding-left: 420px; flex-wrap: nowrap; gap: 8px; margin-bottom: 12px; min-height: 60px; position: relative; z-index: 10;">'
    html = html.replace(old_top_ctrl_tk, new_top_ctrl_tk)

    old_filter_tk = '<div class="filters-container" style="display: flex; flex-direction: row; align-items: center; flex-wrap: wrap; gap: 8px;">'
    new_filter_tk = '<div class="filters-container" style="display: flex; flex-direction: row; align-items: center; flex-wrap: nowrap; gap: 8px;">'
    html = html.replace(old_filter_tk, new_filter_tk)

    old_tk_legend_stats = """    <div class="color-legend">
        <span class="legend-title">Tồn kho:</span>
        <span class="legend-item"><span class="legend-dot ld-green"></span>&lt; 30</span>
        <span class="legend-item"><span class="legend-dot ld-yellow"></span>30 – 50</span>
        <span class="legend-item"><span class="legend-dot ld-orange"></span>50 – 60</span>
        <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 60</span>
    </div>
    </div>
    <div class="stats-bar" style="margin-bottom: 0;">
        <div class="stat blue"><div class="stat-num" id="tk-stat-st">197</div><div class="stat-label">Tổng ST có tồn</div></div>
        <div class="stat yellow"><div class="stat-num" id="tk-stat-total">25,487</div><div class="stat-label">Tổng rổ</div></div>
        <div class="stat green"><div class="stat-num" id="tk-stat-types">9</div><div class="stat-label">Loại rổ</div></div>
        <button class="btn-export" onclick="exportTonKho()">📥 Tải Excel</button>
    </div>"""

    new_tk_legend_stats = """    <div style="display: flex; flex-direction: row; align-items: center; gap: 12px; flex-wrap: nowrap; width: 100%;">
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
    
    html = html.replace(old_tk_legend_stats, new_tk_legend_stats)

    html = html.replace('<div class="table-wrap" style="max-height:calc(100vh - 320px); overflow-y:auto;">',
                        '<div class="table-wrap" style="max-height:calc(100vh - 160px); overflow-y:auto;">')


    # Thu Hồi
    old_top_ctrl_th = '<div class="top-controls-thuhoi" style="display: flex; flex-direction: row; align-items: flex-start; justify-content: flex-start; padding-left: 420px; flex-wrap: wrap; gap: 12px; margin-bottom: 12px; min-height: 80px; position: relative; z-index: 10;">'
    new_top_ctrl_th = '<div class="top-controls-thuhoi" style="display: flex; flex-direction: column; align-items: stretch; justify-content: flex-start; padding-left: 420px; flex-wrap: nowrap; gap: 8px; margin-bottom: 12px; min-height: 60px; position: relative; z-index: 10;">'
    html = html.replace(old_top_ctrl_th, new_top_ctrl_th)

    old_filter_th = '<div class="filters-container-thuhoi" style="display: flex; flex-direction: row; align-items: center; flex-wrap: wrap; gap: 8px;">'
    new_filter_th = '<div class="filters-container-thuhoi" style="display: flex; flex-direction: row; align-items: center; flex-wrap: nowrap; gap: 8px;">'
    html = html.replace(old_filter_th, new_filter_th)

    old_th_legend_stats = """    <div class="color-legend" style="margin-bottom: 0;">
        <span class="legend-title">Chênh lệch:</span>
        <span class="legend-item"><span class="legend-dot ld-green"></span>0 (đủ)</span>
        <span class="legend-item"><span class="legend-dot ld-yellow"></span>&lt; 10</span>
        <span class="legend-item"><span class="legend-dot ld-orange"></span>10 – 30</span>
        <span class="legend-item"><span class="legend-dot ld-red"></span>&gt; 30</span>
    </div>
    </div>
    <div class="stats-bar compact" style="margin-bottom: 0;">
        <div class="stat red"><div class="stat-num">113</div><div class="stat-label">Lượt chưa thu</div></div>
        <div class="stat green"><div class="stat-num">865</div><div class="stat-label">Lượt đã thu</div></div>
        <div class="stat blue"><div class="stat-num">111,940</div><div class="stat-label">Tổng SL Giao</div></div>
        <div class="stat green"><div class="stat-num">109,262</div><div class="stat-label">Tổng SL Thu</div></div>
        <button class="btn-export" onclick="exportThuHoi()" style="align-self:center;padding:5px 12px;font-size:11px;">📥 Excel</button>
    </div>"""

    new_th_legend_stats = """    <div style="display: flex; flex-direction: row; align-items: center; gap: 12px; flex-wrap: nowrap; width: 100%;">
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
    
    html = html.replace(old_th_legend_stats, new_th_legend_stats)

    html = html.replace('<div style="max-height:calc(100vh - 280px); overflow-y:auto;">\n        <table class="data-table" id="trip-table">',
                        '<div style="max-height:calc(100vh - 160px); overflow-y:auto;">\n        <table class="data-table" id="trip-table">')

    # Fix Map
    old_map_top = '<div class="map-top" style="display:flex; justify-content:flex-start; align-items:center; flex-wrap:wrap; gap:12px; padding-left:420px; margin-bottom:12px; position:relative; z-index:10; min-height:80px;">'
    new_map_top = '<div class="map-top" style="display:flex; justify-content:flex-start; align-items:center; flex-wrap:nowrap; gap:12px; padding-left:420px; margin-bottom:12px; position:relative; z-index:10; min-height:60px;">'
    html = html.replace(old_map_top, new_map_top)

    html = html.replace('<div id="map" style="flex:1; width:100%; min-height:400px; border-radius:12px; border:1px solid var(--border); box-shadow:0 4px 12px rgba(0,0,0,0.05); z-index:1;"></div>',
                        '<div id="map" style="flex:1; width:100%; min-height:calc(100vh - 140px); border-radius:12px; border:1px solid var(--border); box-shadow:0 4px 12px rgba(0,0,0,0.05); z-index:1;"></div>')


    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    fix_index()
