# Dashboard Rổ — Quy tắc dự án

> File KI chính (51+ mục) nằm tại: `G:\My Drive\ANTIGRAVITY\PROJECT_STATE.md`
> Đọc file đó để nắm toàn bộ bối cảnh và quy tắc hệ thống.

## Quy tắc riêng cho repo dashboard-ro

### Đường dẫn
- Thư mục dự án: `G:\My Drive\ANTIGRAVITY\Tro_Ly\dashboard-ro\`
- KHÔNG BAO GIỜ dùng ổ D. Mọi thao tác trên ổ G.

### Tự động hóa (KI-57)
- Trợ lý tự chạy pipeline: script Python → git add → commit → push.
- Không yêu cầu người dùng chạy tay bất kỳ thứ gì.
- Push phải xóa biến giả: `$env:GITHUB_TOKEN=""; git push origin master`
- Push cả 2 nhánh: `master` và `master:main`.

### Kiến trúc file (KI-52, KI-53, KI-54, KI-55)
- `index.html`: Trang chính. Không nhét form/component lớn vào Header.
- `tasks.html`: Tab Công việc (iframe). Sửa layout → sửa file này, không kéo ra index.
- `tele.html`: Tab Thu hồi (iframe). Tương tự tasks.html.
- HTML Markers (`<!-- TONKHO_TBODY_START -->`, `<!-- CAL_GRID_START -->`...): TUYỆT ĐỐI không xóa.

### Encoding (KI-56)
- Mọi file `.html` phải có `<meta charset="UTF-8">` trong `<head>`.
- Script Python ghi HTML dùng `encoding='utf-8'`.

### Pipeline chuẩn
```
1. python update_store_data.py
2. python update_excel_data.py
3. git add index.html tele.html tasks.html
4. git commit -m "Auto update <timestamp>"
5. $env:GITHUB_TOKEN=""; git push origin master; git push origin master:main
```

### Nút "Cập nhật" trên Dashboard (KI-66)
- Header có nút **🔄 Cập nhật** gọi `http://localhost:5588/update`.
- Backend: `update_server.py` chạy trên máy local, lắng nghe port 5588.
- Khi bấm nút: server chạy toàn bộ pipeline → git push → trả kết quả JSON.
- Có popup thông báo thành công/lỗi chi tiết từng bước.
- Nếu server chưa chạy → popup hướng dẫn: `python update_server.py`.
- Sau khi thành công → tự cập nhật timestamp trên trang + auto reload sau 3 giây.
- File liên quan: `update_server.py`, `inject_update_btn.py`.

### Mã loại rổ Trip — Mapping quan trọng (KI-67)
Khi thêm/sửa loại rổ, phải đồng bộ **TẤT CẢ** các vị trí sau:

**Trong `index.html` (JS):**
1. `BASKET_NAMES` — Tên hiển thị của mã rổ
2. `COUNTABLE_CODES` — Set các mã rổ được tính vào giao/thu
3. `RECOVERABLE_CODES` — Mảng các mã rổ có thể thu hồi
4. `BASKET_WAREHOUSE` — Kho (Rau/Đông Mát/Khô/Thịt Cá SCF) của mã rổ
5. **Dropdown `basket-dd`** — Checkbox filter trong tab Thu hồi (HTML)

**Trong `update_excel_data.py` (Python):**
6. `COUNTABLE_TRIP_CODES` — Set mã rổ được đếm trong trip

**Bảng mapping hiện tại:**
| Mã cũ | Mã mới | Tên | Kho |
|-------|--------|-----|-----|
| CC00392 | B0018 | Rổ đen có nắp | Thịt Cá SCF |
| B0001 | — | Seedlog - Thùng tote xanh lá | Khô |
| B0012 | — | KRC Rổ nhựa đen xếp chồng quai đỏ | Rau |
| B0015 | — | Rổ ABA đông mát | Đông Mát |
| B0016 | — | Tote ABA đông mát | Đông Mát |
| B0017 | — | Tote đỏ bánh tươi | Rau |

> **Lưu ý:** Mã `B0018` đã thay thế `CC00392` trong dữ liệu trip thực tế.
> Cả 2 mã vẫn cần tồn tại trong code (backward compatible).
> Nếu có mã rổ mới xuất hiện trong trip data mà chưa có trong mapping → dashboard sẽ KHÔNG hiển thị rổ đó trong tổng quan thu hồi.

### Header Layout (KI-68)
- Thứ tự nút trong header: **Cập nhật** → **Giao diện** → **Timestamp**
- Header row có `z-index: 20` để không bị filter controls bên dưới đè lên.
- Container flex có `flex-wrap: wrap` cho responsive.

# Global Git Sync Rule
Whenever you modify project files, you MUST ALWAYS run a terminal command to commit and push the changes to GitHub. Since this is an automated process, you MUST clear the GitHub token from the environment variable before pushing to avoid authentication errors. Use this exact command structure: `git add . && git commit -m "Your commit message" && $env:GITHUB_TOKEN=""; git push origin master`. Do NOT forget this step after any modifications.

