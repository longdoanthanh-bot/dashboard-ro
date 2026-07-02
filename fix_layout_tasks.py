import re

def fix_tasks_layout():
    with open('tasks.html', 'r', encoding='utf-8') as f:
        html = f.read()

    pattern = re.compile(r'<div class="top-row".*?<!-- ADD TASK FORM — RIGHT SIDE.*?<div class="add-form">.*?</div></div>\s*</div>\s*<!-- STATS — LEFT SIDE.*?<div class="stats-row".*?</div>\s*</div>\s*</div>', re.DOTALL)
    
    match = pattern.search(html)
    if not match:
        print("Tasks controls not found!")
        return

    add_form = """
        <div class="add-form">
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
            </div>
        </div>
    """

    stats = """
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
    """

    new_tasks = f"""<div class="top-row" style="display: flex; flex-direction: column; align-items: stretch; justify-content: flex-start; padding-left: 0; flex-wrap: nowrap; gap: 8px; margin-bottom: 12px; position: relative; z-index: 10;">
    <!-- Row 1: Logo Space + Add Form -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: nowrap; align-items: flex-start; width: 100%;">
        <div style="width: 420px; flex-shrink: 0; min-height: 90px;"></div>
        {add_form}
    </div>
    
    <!-- Row 2: Stats Block on left -->
    <div style="display: flex; flex-direction: row; gap: 12px; flex-wrap: nowrap; width: 100%;">
        <div class="stats-row" style="width: 420px; flex-shrink: 0; justify-content: flex-start; gap: 8px; padding-left: 12px; margin-bottom: 0;">
            {stats}
        </div>
        <div style="flex: 1;"></div>
    </div>
</div>"""

    html = html[:match.start()] + new_tasks + html[match.end():]

    with open('tasks.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    fix_tasks_layout()
