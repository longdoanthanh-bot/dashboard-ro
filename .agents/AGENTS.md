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

# Global Git Sync Rule
Whenever you modify project files, you MUST ALWAYS run a terminal command to commit and push the changes to GitHub. Since this is an automated process, you MUST clear the GitHub token from the environment variable before pushing to avoid authentication errors. Use this exact command structure: `git add . && git commit -m "Your commit message" && $env:GITHUB_TOKEN=""; git push origin master`. Do NOT forget this step after any modifications.
