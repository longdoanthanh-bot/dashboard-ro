import re

def fix_tasks_html():
    with open('tasks.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The current top-row
    # We will replace the entire .add-form to have exactly 2 lines.
    
    old_add_form_css = """.add-form {
    flex:1; background:var(--card); border:1px solid var(--border); border-radius:8px;
    padding:8px 14px; display:flex; align-items:flex-end; gap:10px; flex-wrap:wrap;
}"""
    new_add_form_css = """.add-form {
    flex:1; background:var(--card); border:1px solid var(--border); border-radius:8px;
    padding:8px 14px; display:flex; flex-direction:column; gap:8px;
}
.add-form-row { display:flex; gap:10px; align-items:flex-end; width:100%; flex-wrap:nowrap; }"""
    html = html.replace(old_add_form_css, new_add_form_css)

    # Reconstruct the HTML of add-form
    form_start_idx = html.find('<div class="add-form">')
    form_end_idx = html.find('</div>\n        \n        <!-- STATS')
    
    if form_start_idx != -1 and form_end_idx != -1:
        new_form_html = """<div class="add-form">
            <div class="add-form-row">
                <div class="form-title" style="margin-right:10px; padding-bottom:6px;">➕ Thêm task mới</div>
                <div class="form-group" style="flex:1;">
                    <label>Tiêu đề</label>
                    <input class="form-input" type="text" id="new-title" placeholder="Nhập tiêu đề...">
                </div>
                <div class="form-group" style="flex:2;">
                    <label>Nội dung</label>
                    <textarea class="form-input" id="new-desc" rows="1" placeholder="Mỗi dòng = 1 task nhỏ..." style="resize:vertical;min-height:28px;padding-top:4px;"></textarea>
                </div>
            </div>
            <div class="add-form-row">
                <div class="form-group" style="flex:1;">
                    <label>Deadline</label>
                    <input class="form-input" type="datetime-local" id="new-deadline" style="width:100%;">
                </div>
                <div class="form-group" style="flex:0 0 100px;">
                    <label>Ưu tiên</label>
                    <select class="form-input" id="new-priority" style="min-width:90px;width:100%;">
                        <option value="3">🟢 P3</option>
                        <option value="2">🟠 P2</option>
                        <option value="1">🔴 P1</option>
                    </select>
                </div>
                <button class="btn-create" onclick="createTask()" style="height:32px; padding:0 24px;">Tạo</button>
                <button class="header-btn" onclick="exportExcel()" style="height:32px; padding:0 12px; margin-left:0;">📥 Excel</button>
            </div>"""
        html = html[:form_start_idx] + new_form_html + html[form_end_idx:]

    # Reduce min-height of top-row
    html = html.replace('min-height: 80px;', 'min-height: 60px;')
    
    # Also adjust the layout of top-row to put add-form and stats-row side-by-side if they wrap.
    # Currently it's flex-wrap: wrap, which is fine, but they might be too large.
    html = html.replace('<div class="top-row" style="display: flex; flex-direction: row; align-items: flex-start; justify-content: flex-start; padding-left: 420px; flex-wrap: wrap; gap: 12px; margin-bottom: 16px; min-height: 80px; position: relative; z-index: 10;">',
                        '<div class="top-row" style="display: flex; flex-direction: row; align-items: stretch; justify-content: space-between; padding-left: 420px; flex-wrap: nowrap; gap: 12px; margin-bottom: 16px; min-height: 60px; position: relative; z-index: 10;">')

    with open('tasks.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    fix_tasks_html()
