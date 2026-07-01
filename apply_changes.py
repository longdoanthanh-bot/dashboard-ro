import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS
html = html.replace('.cal-day.active { border-width:2px; }', '.cal-day.active { border-width:2px; border-color:var(--blue); background:rgba(108,140,255,0.08); }')

# 2. filterDateRange
old_filter = """function filterDateRange() {
    const from = document.getElementById('date-from').value;
    const to = document.getElementById('date-to').value;
    document.querySelectorAll('#trip-date-bar .cal-day').forEach(d => {
        const iso = d.dataset.iso;
        const inRange = iso >= from && iso <= to;
        if(inRange) { d.classList.add('active'); d.classList.remove('out-range'); }
        else { d.classList.remove('active'); d.classList.add('out-range'); }
    });
    renderTripTable();
}"""
new_filter = """function filterDateRange() {
    let from = document.getElementById('date-from').value;
    let to = document.getElementById('date-to').value;
    try {
        if(from && !from.match(/^\d{4}-\d{2}-\d{2}$/)) from = new Date(from).toISOString().split('T')[0];
        if(to && !to.match(/^\d{4}-\d{2}-\d{2}$/)) to = new Date(to).toISOString().split('T')[0];
    } catch(e) {}
    document.querySelectorAll('#trip-date-bar .cal-day').forEach(d => {
        const iso = d.dataset.iso;
        if(!iso) return;
        let inRange = false;
        if (from && to) inRange = (iso >= from && iso <= to);
        else if (from) inRange = (iso >= from);
        else if (to) inRange = (iso <= to);
        else inRange = true;
        if(inRange) { d.classList.add('active'); d.classList.remove('out-range'); }
        else { d.classList.remove('active'); d.classList.add('out-range'); }
    });
    renderTripTable();
}"""
html = html.replace(old_filter, new_filter)

# 3. HTML Summary Panel
old_html = """        <button class="btn-export" onclick="exportThuHoi()" style="align-self:center;padding:5px 12px;font-size:11px;">📥 Excel</button>
    </div>
    <div class="cal-bar" id="trip-date-bar">"""
new_html = """        <button class="btn-export" onclick="exportThuHoi()" style="align-self:center;padding:5px 12px;font-size:11px;">📥 Excel</button>
    </div>
    <div class="basket-summary-panel" id="basket-summary" style="display:none; background:var(--bg); border:1px dashed var(--red); border-radius:8px; padding:10px 14px; margin-bottom:10px;">
        <div style="font-size:11px; font-weight:700; color:var(--text2); margin-bottom:8px; text-transform:uppercase;">Chi tiết các loại rổ chưa thu (tổng quan)</div>
        <div id="basket-summary-content" style="display:flex; flex-wrap:wrap; gap:8px;"></div>
    </div>
    <div class="cal-bar" id="trip-date-bar">"""
html = html.replace(old_html, new_html)

# 4. renderTripTable replacements
old_render_1 = """    stores.forEach(s => {
        let g=0, t=0;
        const activeWh = document.getElementById('trip-wh-filter')?.value || '';
        for(const [ic, [ig, it]] of Object.entries(s.items)) {
            if(!COUNTABLE_CODES.has(ic)) continue;
            if(!useAll && activeCodes && !activeCodes.includes(ic)) continue;
            if(activeWh && (BASKET_WAREHOUSE[ic]||'') !== activeWh) continue;
            g += ig; t += it;
        }
        s.fg = g; s.ft = t;
    });
    stores = stores.filter(s => s.fg>0 || s.ft>0);
    if(searchQ) stores = stores.filter(s => s.code.toLowerCase().includes(searchQ) || s.name.toLowerCase().includes(searchQ));
    stores.forEach(s => {
        if(s.ft === 0) s.status = 'none';
        else if(s.ft < s.fg) s.status = 'partial';
        else s.status = 'full';
    });
    const activeS = getActiveStatuses();
    if(activeS) stores = stores.filter(s => activeS.has(s.status));
    stores.sort((a,b) => (b.fg-b.ft) - (a.fg-a.ft));
    let allNr=0, allRc=0, allG=0, allT=0;
    stores.forEach(s => { allG+=s.fg; allT+=s.ft; if(s.ft>=s.fg && s.fg>0) allRc++; else allNr++; });"""

new_render_1 = """    stores.forEach(s => {
        let g=0, t=0;
        s.itemStatuses = new Set();
        const activeWh = document.getElementById('trip-wh-filter')?.value || '';
        for(const [ic, [ig, it]] of Object.entries(s.items)) {
            if(!COUNTABLE_CODES.has(ic)) continue;
            if(!useAll && activeCodes && !activeCodes.includes(ic)) continue;
            if(activeWh && (BASKET_WAREHOUSE[ic]||'') !== activeWh) continue;
            g += ig; t += it;
            if (ig > 0 && it === 0) s.itemStatuses.add('none');
            else if (ig > 0 && it < ig) s.itemStatuses.add('partial');
            else if (ig > 0 && it >= ig) s.itemStatuses.add('full');
        }
        s.fg = g; s.ft = t;
    });
    stores = stores.filter(s => s.fg>0 || s.ft>0);
    if(searchQ) stores = stores.filter(s => s.code.toLowerCase().includes(searchQ) || s.name.toLowerCase().includes(searchQ));
    stores.forEach(s => {
        if(s.ft === 0) s.status = 'none';
        else if(s.ft < s.fg) s.status = 'partial';
        else s.status = 'full';
    });
    const activeS = getActiveStatuses();
    if(activeS) stores = stores.filter(s => activeS.has(s.status) || (s.itemStatuses && Array.from(s.itemStatuses).some(st => activeS.has(st))));
    stores.sort((a,b) => (b.fg-b.ft) - (a.fg-a.ft));
    let allNr=0, allRc=0, allG=0, allT=0;
    let missingBaskets = {};
    stores.forEach(s => { 
        allG+=s.fg; allT+=s.ft; if(s.ft>=s.fg && s.fg>0) allRc++; else allNr++; 
        const activeWh = document.getElementById('trip-wh-filter')?.value || '';
        for(const [ic, [ig, it]] of Object.entries(s.items)) {
            if(!COUNTABLE_CODES.has(ic)) continue;
            const useAllLocal = (activeCodes === null);
            if(!useAllLocal && activeCodes && !activeCodes.includes(ic)) continue;
            if(activeWh && (BASKET_WAREHOUSE[ic]||'') !== activeWh) continue;
            const diff = ig - it;
            if (diff > 0) {
                missingBaskets[ic] = (missingBaskets[ic] || 0) + diff;
            }
        }
    });
    
    const bSumPanel = document.getElementById('basket-summary');
    const bSumContent = document.getElementById('basket-summary-content');
    if (bSumPanel && bSumContent) {
        const mKeys = Object.keys(missingBaskets).sort((a,b) => missingBaskets[b] - missingBaskets[a]);
        if (mKeys.length > 0) {
            bSumPanel.style.display = 'block';
            bSumContent.innerHTML = mKeys.map(ic => {
                const bName = BASKET_NAMES[ic] || ic;
                return `<div style="background:rgba(248,113,113,0.1); border:1px solid rgba(248,113,113,0.3); color:var(--red); padding:4px 10px; border-radius:6px; font-size:11px; font-weight:600; display:flex; align-items:center; gap:6px;">
                    ${bName}: <span style="font-size:13px; font-weight:800;">${fmt(missingBaskets[ic])}</span>
                </div>`;
            }).join('');
        } else {
            bSumPanel.style.display = 'none';
            bSumContent.innerHTML = '';
        }
    }"""
html = html.replace(old_render_1, new_render_1)

old_render_2 = """        for(const [ic, it] of detailItems) {
            const cl=it[0]-it[1], clC=cl>0?'high':'';
            dr += `<tr><td>${BASKET_NAMES[ic]||ic}</td><td class="num">${fmt(it[0])}</td><td class="num">${fmt(it[1])}</td><td class="num ${clC}">${fmt(cl)}</td></tr>`;
        }
        const tr = document.createElement('tr');
        tr.className = `${rowCls} trip-row`;
        tr.onclick = function(){ toggleExpand(this); };
        tr.innerHTML = `<td class="stt">${i+1}</td><td>${s.code}</td><td>${s.name}</td><td class="num">${fmt(g)}</td><td class="${thuCls}">${fmt(t)}</td><td class="${diffCls}">${fmt(diff)}</td><td class="${statusCls}">${statusLabel}</td>`;"""
new_render_2 = """        for(const [ic, it] of detailItems) {
            const cl=it[0]-it[1], clC=cl>0?'high':'';
            let itemWarn = '';
            if(it[0]>0 && it[1]===0) itemWarn = ' <span style="color:var(--red); font-size:10px; font-weight:bold;">(Không thu)</span>';
            else if(it[0]>0 && it[1]<it[0]) itemWarn = ' <span style="color:var(--orange); font-size:10px; font-weight:bold;">(Thu thiếu)</span>';
            dr += `<tr><td>${BASKET_NAMES[ic]||ic}${itemWarn}</td><td class="num">${fmt(it[0])}</td><td class="num">${fmt(it[1])}</td><td class="num ${clC}">${fmt(cl)}</td></tr>`;
        }
        const tr = document.createElement('tr');
        tr.className = `${rowCls} trip-row`;
        tr.onclick = function(){ toggleExpand(this); };
        let warnIcon = (s.itemStatuses && s.itemStatuses.has('none') && s.status !== 'none') ? ' <span style="color:var(--red); font-weight:bold; font-size:12px;" title="Cảnh báo: Có loại rổ hoàn toàn không thu">⚠</span>' : '';
        tr.innerHTML = `<td class="stt">${i+1}</td><td>${s.code}</td><td>${s.name}${warnIcon}</td><td class="num">${fmt(g)}</td><td class="${thuCls}">${fmt(t)}</td><td class="${diffCls}">${fmt(diff)}</td><td class="${statusCls}">${statusLabel}</td>`;"""
html = html.replace(old_render_2, new_render_2)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
