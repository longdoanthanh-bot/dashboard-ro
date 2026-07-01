"""Add HTML markers that update_excel_data.py needs"""
import re

with open('index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

changes = 0

# 1. Add TONKHO_TBODY markers around the tonkho <tbody>...</tbody>
# Find the tbody inside tonkho-table
pattern_tbody = re.compile(
    r'(<table class="data-table" id="tonkho-table">.*?</thead>\s*)'  # everything up to end of thead
    r'(<tbody>.*?</tbody>)'  # the tbody block
    r'(\s*</table>)',
    re.DOTALL
)
match = pattern_tbody.search(content)
if match:
    before = match.group(1)
    tbody = match.group(2)
    after = match.group(3)
    if '<!-- TONKHO_TBODY_START -->' not in tbody:
        new_section = before + '<!-- TONKHO_TBODY_START -->\n' + tbody + '\n<!-- TONKHO_TBODY_END -->' + after
        content = content[:match.start()] + new_section + content[match.end():]
        changes += 1
        print("[OK] Added TONKHO_TBODY markers")
    else:
        print("[SKIP] TONKHO_TBODY markers already exist")
else:
    print("[WARN] Could not find tonkho tbody")

# 2. Add CAL_GRID markers around the cal-grid div contents
pattern_cal = re.compile(
    r'(<div class="cal-grid">)\s*'
    r'(.*?)'
    r'(\s*</div>\s*</div>\s*</div>\s*</div>)',  # closing divs of cal-bar structure
    re.DOTALL
)
match_cal = pattern_cal.search(content)
if match_cal:
    cal_open = match_cal.group(1)
    cal_content = match_cal.group(2)
    cal_close = match_cal.group(3)
    if '<!-- CAL_GRID_START -->' not in cal_content:
        new_cal = cal_open + '\n<!-- CAL_GRID_START -->\n' + cal_content.strip() + '\n<!-- CAL_GRID_END -->\n' + cal_close
        content = content[:match_cal.start()] + new_cal + content[match_cal.end():]
        changes += 1
        print("[OK] Added CAL_GRID markers")
    else:
        print("[SKIP] CAL_GRID markers already exist")
else:
    print("[WARN] Could not find cal-grid")

if changes > 0:
    with open('index.html', 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print(f"[DONE] {changes} marker(s) added")
else:
    print("[DONE] No changes needed")
