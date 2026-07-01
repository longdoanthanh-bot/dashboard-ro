# KI — Dashboard Rổ KingFoodmart

> Đây là bộ quy tắc bắt buộc cho trợ lý AI khi làm việc với dự án này.
> Mọi vi phạm đều dẫn đến hậu quả nghiêm trọng (phá layout, mất dữ liệu, lỗi font).

---

## 1. Đường dẫn & Lưu trữ

- **Thư mục dự án duy nhất:** `G:\My Drive\ANTIGRAVITY\Tro_Ly\dashboard-ro\`
- **KHÔNG BAO GIỜ** dùng ổ D hay bất kỳ đường dẫn nào khác. Mọi file code, script, HTML đều nằm ở ổ G.
- Trong code Python, dùng `os.path.dirname(os.path.abspath(__file__))` làm gốc (relative path). Chỉ hardcode đường dẫn ổ G cho các file dữ liệu nguồn bên ngoài dự án (Excel trên Google Drive).

---

## 2. Tự động hóa — KHÔNG chạy tay

- **Trợ lý phải TỰ CHẠY** toàn bộ pipeline: chạy script Python -> git add -> git commit -> git push. Không bao giờ yêu cầu người dùng mở Terminal hay click file `.bat`.
- **Khi push Github**, phải xóa biến môi trường giả trước:
  - PowerShell: `$env:GITHUB_TOKEN=""; git push origin master`
  - Hoặc cmd: `cmd.exe /c "set GITHUB_TOKEN= && git push origin master && git push origin master:main"`
- **Push cả 2 nhánh:** `master` và `master:main` (Github Pages đọc từ `main`).
- Sau khi push, ghi rõ kết quả (thành công / thất bại) cho người dùng. Không nói "anh tự chạy nhé".

---

## 3. Cập nhật thời gian

- Mỗi khi có bất kỳ thay đổi nào (dữ liệu hoặc giao diện), **LUÔN cập nhật** text `Cập nhật: <ngày> <giờ>` trên header Dashboard thành thời gian hiện tại.

---

## 4. Kiến trúc file — KHÔNG được phá

| File | Vai trò | Quy tắc |
|------|---------|---------|
| `index.html` | Trang chính (4 tab: Tồn kho, Thu hồi, Sơ đồ, Công việc) | Không nhét form/component lớn vào `.header` hay `#header-filters`. Header chỉ dùng cho dropdown lọc nhỏ gọn và nút bấm. |
| `tasks.html` | Nội dung Tab Công việc, nhúng qua `<iframe>` | Mọi thay đổi layout Tab Công việc (xếp thống kê, form thêm task) phải sửa **trực tiếp trong file này**, không bốc ra `index.html`. |
| `tele.html` | Nội dung Tab Thu hồi | Tương tự `tasks.html` — sửa trong file, không kéo ra ngoài. |
| `update_store_data.py` | Nạp dữ liệu cửa hàng (JSON -> `STORE_COORDS`) | Giữ nguyên cấu trúc regex tìm `const STORE_COORDS = [...]`. |
| `update_excel_data.py` | Nạp dữ liệu Tồn kho (Excel -> bảng HTML) và Trip | Giữ nguyên cấu trúc regex tìm `TRIP_DATA`, `TONKHO_TBODY`, `CAL_GRID`, date-picker. |
| `run_update.bat` | Pipeline tự động: check -> update -> commit -> push | Không sửa trừ khi có lý do chính đáng. |

---

## 5. HTML Markers — TUYỆT ĐỐI không xóa

Các script Python dùng comment HTML làm điểm neo để chèn dữ liệu. **Xóa chúng = hệ thống liệt.**

```
<!-- TONKHO_TBODY_START --> ... <!-- TONKHO_TBODY_END -->
<!-- CAL_GRID_START --> ... <!-- CAL_GRID_END -->
```

Khi refactor HTML/CSS, phải **bảo tồn 100%** các cặp comment này ở đúng vị trí.

---

## 6. Font chữ & Encoding

- Mọi file `.html` phải có `<meta charset="UTF-8">` trong `<head>`.
- Script Python ghi file HTML phải dùng `encoding='utf-8'`.
- Nếu tạo file HTML mới hoặc thay thế, **bắt buộc** thêm thẻ meta charset.
- Mục đích: ngăn lỗi mojibake (vỡ font tiếng Việt: Tất cả bị hiện thành ký tự lạ).

---

## 7. Quy tắc sửa giao diện

1. **Không nhét component lớn vào Header:** Form "Thêm task", Map Controls, bảng thống kê lớn -> để trong panel chính, không đưa lên header.
2. **Giữ nguyên bố trí các tab khác khi sửa 1 tab:** Nếu người dùng yêu cầu sửa Tab Công việc, thì Tab Tồn kho, Thu hồi, Sơ đồ phải giữ nguyên 100%. Không "tiện tay" sửa.
3. **Iframe = file riêng:** Tab Công việc và Tab Thu hồi dùng iframe. Sửa layout bên trong -> sửa file `.html` tương ứng. Không kéo nội dung iframe ra `index.html`.
4. **Kiểm tra trước khi push:** Sau khi sửa HTML, kiểm tra nhanh bằng `Select-String` xem các marker, biến JS, cấu trúc quan trọng còn nguyên không.

---

## 8. Git — Xử lý xung đột

- Nếu push bị reject (remote ahead), dùng: `git pull --rebase origin master` rồi push lại.
- Nếu rebase bị conflict, xử lý conflict (hoặc `git rebase --abort` rồi reset lại) — **KHÔNG để treo** giữa chừng.
- Ưu tiên `git push -f` nếu chắc chắn local mới hơn remote (dùng `cmd.exe /c` để tránh lỗi token).

---

## 9. Tóm tắt Pipeline chạy đúng

```
1. python update_store_data.py    -> Cập nhật STORE_COORDS + timestamp
2. python update_excel_data.py    -> Cập nhật TRIP_DATA + TONKHO bảng + Calendar + timestamp
3. git add index.html tele.html tasks.html
4. git commit -m "Auto update <timestamp>"
5. $env:GITHUB_TOKEN=""; git push origin master; git push origin master:main
```

Trợ lý phải chạy toàn bộ 5 bước này tự động, không hỏi người dùng.
