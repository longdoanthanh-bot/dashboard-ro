import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Change missingBaskets calculation
old_missing = """              const diff = ig - it;
              if (diff > 0) {
                  missingBaskets[ic] = (missingBaskets[ic] || 0) + diff;
              }"""
new_missing = """              if (ig > 0 && it === 0) {
                  missingBaskets[ic] = (missingBaskets[ic] || 0) + ig;
              }"""
html = html.replace(old_missing, new_missing)

# 2. Fix store status in table rendering
old_status = """        let rowCls,statusCls,statusLabel;
        if(s.status==='none') { rowCls='row-status-none'; statusCls='status-none'; statusLabel='✗ Không thu'; }
        else if(s.status==='partial') { rowCls='row-status-partial'; statusCls=diff>30?'status-partial-high':diff>=10?'status-partial-mid':'status-partial-low'; statusLabel='⚠ Thu 1 phần'; }
        else { rowCls='row-status-full'; statusCls='status-full'; statusLabel='✓ Đã thu hết'; }"""

new_status = """        let itemStatus = s.status;
        if (window.activeMissingFilter) {
            if (t === 0 && g > 0) itemStatus = 'none';
            else if (t < g && g > 0) itemStatus = 'partial';
            else itemStatus = 'full';
        }
        let rowCls,statusCls,statusLabel;
        if(itemStatus==='none') { rowCls='row-status-none'; statusCls='status-none'; statusLabel='✗ Không thu'; }
        else if(itemStatus==='partial') { rowCls='row-status-partial'; statusCls=diff>30?'status-partial-high':diff>=10?'status-partial-mid':'status-partial-low'; statusLabel='⚠ Thu 1 phần'; }
        else { rowCls='row-status-full'; statusCls='status-full'; statusLabel='✓ Đã thu hết'; }"""

html = html.replace(old_status, new_status)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
