import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add missing </div></div> to trip-date-bar inside thuhoi-header-filters
content = re.sub(
    r'(<div class="cal-day active".*?</div>)\s*</div>\s*<div class="filter-row"',
    r'\1\n                </div>\n            </div>\n        </div>\n        <div class="filter-row"',
    content
)

# 2. Fix the extra </div></div> in panel-thuhoi and remove flex: 1 from basket-summary
content = re.sub(
    r'<div class="basket-summary-panel" id="basket-summary" style="display:none; flex: 1; background:var\(--bg\); border:1px dashed var\(--red\); border-radius:8px; padding:10px 14px;">\s*(<div style="font-size:11px; font-weight:700; color:var\(--text2\); margin-bottom:8px; text-transform:uppercase;">.*?</div>)\s*(<div id="basket-summary-content" style="display:flex; flex-wrap:wrap; gap:8px;"></div>)\s*</div>\s*</div>\s*</div>',
    r'<div class="basket-summary-panel" id="basket-summary" style="display:none; margin-bottom: 10px; background:var(--bg); border:1px dashed var(--red); border-radius:8px; padding:10px 14px;">\n        \1\n        \2\n    </div>',
    content,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("DOM errors fixed successfully")
