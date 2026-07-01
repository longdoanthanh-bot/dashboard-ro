import codecs

with codecs.open(r'G:\My Drive\ANTIGRAVITY\PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the last KI entry (KI-51) and append new ones after it
new_ki_entries = """| **KI-52**| Không phá HTML Markers | Các script Python (`update_excel_data.py`) dùng comment HTML (`<!-- TONKHO_TBODY_START -->`, `<!-- CAL_GRID_START -->`, v.v.) làm điểm neo chèn dữ liệu. Khi refactor HTML/CSS, TUYỆT ĐỐI bảo tồn 100% các cặp comment này. Xóa = hệ thống nạp dữ liệu liệt. |
| **KI-53**| Không nhét form vào Header | Các form nhập liệu lớn (Add Task, Map Controls) tuyệt đối không đưa vào `.header` hay `#header-filters`. Header chỉ dùng cho dropdown lọc nhỏ gọn và nút bấm. Nhét form to = phá vỡ layout toàn web. |
| **KI-54**| Iframe = sửa file riêng | Tab Công việc (`tasks.html`) và Tab Thu hồi (`tele.html`) nhúng qua `<iframe>`. Sửa layout bên trong → sửa đúng file `.html` tương ứng. Không bốc nội dung iframe ra `index.html`. |
| **KI-55**| Giữ nguyên tab khác | Khi người dùng yêu cầu sửa 1 tab, các tab còn lại phải giữ nguyên 100%. Không "tiện tay" sửa lan sang tab khác. |
| **KI-56**| Meta charset UTF-8 | Mọi file `.html` phải có `<meta charset="UTF-8">` trong `<head>`. Script Python ghi HTML phải dùng `encoding='utf-8'`. Ngăn lỗi mojibake vỡ font tiếng Việt. |
| **KI-57**| Tự động push Github | Trợ lý phải tự chạy toàn bộ pipeline (script → git add → commit → push). Không bao giờ yêu cầu người dùng chạy tay. Khi push phải xóa biến giả: `$env:GITHUB_TOKEN=""; git push origin master`. Push cả `master` và `master:main`. |
| **KI-58**| Git xung đột | Push bị reject → `git pull --rebase origin master` rồi push lại. Rebase conflict → abort rồi reset. Không để treo giữa chừng. Ưu tiên `git push -f` qua `cmd.exe /c` nếu chắc chắn local mới hơn. |
"""

# Insert before the last line (which is empty)
if '| **KI-51**|' in content:
    content = content.rstrip() + '\n' + new_ki_entries

with codecs.open(r'G:\My Drive\ANTIGRAVITY\PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Added KI-52 to KI-58 to PROJECT_STATE.md")
