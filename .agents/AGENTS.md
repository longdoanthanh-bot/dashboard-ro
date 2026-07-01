# Quy tắc Cập nhật thời gian
- Mỗi khi có bất kỳ thay đổi nào từ dữ liệu đến format (chỉnh sửa file index.html hoặc các file liên quan), hãy LUÔN LUÔN CẬP NHẬT text "Cập nhật: <ngày> <giờ>" trên header giao diện thành thời gian hiện tại của hệ thống. Đây là một quy tắc bắt buộc.

# Quy trình Tự động hóa & Code (KI)
- Tuyệt đối KHÔNG ĐƯỢC yêu cầu người dùng tự chạy tay các file update (như run_update.bat hay lệnh git push). Trợ lý phải TỰ ĐỘNG CHẠY và push lên cho người dùng.
- Mọi thay đổi mã nguồn, fix lỗi, cập nhật giao diện, ĐỀU PHẢI ĐƯỢC TRỢ LÝ TỰ ĐỘNG PUSH lên Github. Để tránh bị lỗi xác thực do DUMMY TOKEN của hệ thống AI, bắt buộc phải XÓA BIẾN MÔI TRƯỜNG TRƯỚC KHI PUSH (ví dụ chạy lệnh PowerShell: `$env:GITHUB_TOKEN=""; git push origin master`). Hoặc dùng `cmd.exe /c "set GITHUB_TOKEN= && git push origin master"`.
- Tuyệt đối KHÔNG hardcode các đường dẫn ổ cứng (như D:\...) vào code. Phải luôn sử dụng relative path. Mọi thứ hiện đã được chuyển hẳn sang ổ G.

# Quy tắc Bố cục Giao diện & Data Pipeline (Rất quan trọng)
1. **Không nhét các Component lớn vào Header:** Các form nhập liệu (Add Task) hoặc bảng điều khiển phức tạp (Map Controls) tuyệt đối không được đưa vào thẻ Header (`#header-filters`, `.app-header`). Việc nhét form to vào header sẽ phá vỡ hoàn toàn layout chung của web.
2. **Chỉnh sửa Iframe thì phải sửa đúng file:** Tab Công việc (`panel-tasks`) được nhúng qua iframe. Nếu người dùng yêu cầu đổi layout ở Tab Công việc (ví dụ: xếp thống kê hàng ngang, form thêm task ở dưới), phải sửa trực tiếp trong file `tasks.html` (chỉnh CSS `flex-direction`, `order`), tuyệt đối không được bốc các thẻ đó mang ra ngoài `index.html`.
3. **Bảo tồn tuyệt đối các thẻ Comment HTML (Markers):** Các hệ thống nạp dữ liệu bằng Python (như `update_excel_data.py`) dựa vào các đoạn mã comment HTML (`<!-- TONKHO_TBODY_START -->`, `<!-- CAL_GRID_START -->`, v.v.) để chèn dữ liệu mới vào bảng. Khi cấu trúc lại HTML/CSS, TUYỆT ĐỐI KHÔNG xóa các thẻ comment này, nếu xóa hệ thống tự động sẽ bị liệt, số liệu sẽ trở thành rác.
4. **Bảo vệ Font chữ (Encoding):** Mọi file `.html` đều phải có thẻ `<meta charset="UTF-8">` nằm trong `<head>`. Nếu tạo file mới hoặc thay thế file cũ, phải nhớ thêm thẻ này để ngăn chặn triệt để lỗi mojibake (vỡ font chữ tiếng Việt).
