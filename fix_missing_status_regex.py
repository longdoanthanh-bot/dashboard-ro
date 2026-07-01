import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix missingBaskets generation
html = re.sub(r'const diff = ig - it;\s*if \(diff > 0\) {', 'if (ig > 0 && it === 0) {', html)

# 2. Fix TRANG THAI column
old_status = r"let rowCls,statusCls,statusLabel;\s*if\(s\.status==='none'\) \{ rowCls='row-status-none'; statusCls='status-none'; statusLabel='✗ Không thu'; \}\s*else if\(s\.status==='partial'\) \{ rowCls='row-status-partial'; statusCls=diff>30\?'status-partial-high':diff>=10\?'status-partial-mid':'status-partial-low'; statusLabel='⚠ Thu 1 phần'; \}\s*else \{ rowCls='row-status-full'; statusCls='status-full'; statusLabel='✓ Đã thu hết'; \}"

new_status = """let itemStatus = s.status;
        if (window.activeMissingFilter) {
            if (t === 0 && g > 0) itemStatus = 'none';
            else if (t < g && g > 0) itemStatus = 'partial';
            else itemStatus = 'full';
        }
        let rowCls,statusCls,statusLabel;
        if(itemStatus==='none') { rowCls='row-status-none'; statusCls='status-none'; statusLabel='✗ Không thu'; }
        else if(itemStatus==='partial') { rowCls='row-status-partial'; statusCls=diff>30?'status-partial-high':diff>=10?'status-partial-mid':'status-partial-low'; statusLabel='⚠ Thu 1 phần'; }
        else { rowCls='row-status-full'; statusCls='status-full'; statusLabel='✓ Đã thu hết'; }"""

html = re.sub(old_status, new_status, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
