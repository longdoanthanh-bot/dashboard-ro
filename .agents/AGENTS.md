# Dashboard Rổ — Quy tắc dự án

> File KI chính (51+ mục) nằm tại: `G:\My Drive\ANTIGRAVITY\PROJECT_STATE.md`
> Đọc file đó để nắm toàn bộ bối cảnh và quy tắc hệ thống.

## Quy tắc riêng cho repo dashboard-ro

### Đường dẫn
- Thư mục dự án: `C:\Users\Thanh Long\.gemini\antigravity\scratch\dashboard-ro\`
- Repo: `https://github.com/longdoanthanh-bot/dashboard-ro` (private)
- Dashboard: `https://longdoanthanh-bot.github.io/dashboard-ro/`

### Kiến trúc file (KI-52, KI-53, KI-54, KI-55)
- `index.html`: Trang chính. Không nhét form/component lớn vào Header.
- `tasks.html`: Tab Công việc (iframe). Sửa layout → sửa file này, không kéo ra index.
- `tele.html`: Tab Thu hồi (iframe). Tương tự tasks.html.
- HTML Markers (`<!-- TONKHO_TBODY_START -->`, `<!-- CAL_GRID_START -->`...): TUYỆT ĐỐI không xóa.
- `data/`: Thư mục chứa dữ liệu nguồn (Excel, JSON) — được đọc bởi pipeline.
  - `data/Master/` — store_coordinates.json, DS-khu-vuc, Danh sách ST
  - `data/TonKhoRo/` — XNT_*.xlsx (tồn kho rổ)
  - `data/Trip/` — DS-chi-tiet-chuyen-xe_*.xlsx (trip giao/thu)

### Encoding (KI-56)
- Mọi file `.html` phải có `<meta charset="UTF-8">` trong `<head>`.
- Script Python ghi HTML dùng `encoding='utf-8'`.

### Pipeline cập nhật — GitHub Actions (KI-69, thay thế KI-57 & KI-66)

**Trước đây:** Chạy `update_server.py` trên máy local (localhost:5588).
**Hiện tại:** Chạy hoàn toàn trên GitHub Actions — KHÔNG CẦN máy local.

#### Triggers (3 cách kích hoạt):
| Trigger | Khi nào |
|---------|---------|
| `workflow_dispatch` | Bấm nút "🔄 Cập nhật" trên dashboard |
| `schedule: cron 0 */2 * * *` | Tự động mỗi 2 tiếng (backup) |

> ⚠️ **KHÔNG có push trigger** (đã xóa KI-69). Push code → Pages deploy 1-2 phút, không chạy pipeline.

#### Pipeline steps (GitHub Actions):
```
1. Checkout repo (dùng GH_PAT secret)
2. Setup Python 3.11 + pip install pandas openpyxl
3. python check_khuvuc.py  (continue-on-error)
4. python check_st.py      (continue-on-error)
5. python update_store_data.py
6. python update_excel_data.py
7. git add → commit → push origin master + master:main
```

#### Python scripts — Dual-path (KI-70):
Tất cả script dùng env var `DATA_DIR`:
- **Trên GitHub Actions:** `DATA_DIR=$GITHUB_WORKSPACE/data` → đọc từ `data/` trong repo
- **Trên máy local (fallback):** không set `DATA_DIR` → đọc từ Google Drive `G:\My Drive\...`

Scripts đã sửa: `update_store_data.py`, `update_excel_data.py`, `check_khuvuc.py`, `check_st.py`

#### Nút "Cập nhật" trên Dashboard (KI-71, thay thế KI-66):
- Bấm nút → JS gọi GitHub API `workflow_dispatch` (KHÔNG gọi localhost nữa)
- Token PAT lưu trong `localStorage` của browser, nhập 1 lần qua prompt
- Sau khi trigger → `pollWorkflowStatus()` theo dõi real-time mỗi 10 giây
- Workflow xong → popup thành công + auto reload
- Code: hàm `triggerUpdate()` và `pollWorkflowStatus()` trong `index.html`
- Biến: `GH_OWNER`, `GH_REPO`, `GH_WORKFLOW`, `GH_BRANCH`, `GH_PAT`

#### Secrets & Security (KI-72):
- Repo secret `GH_PAT`: Personal Access Token (scope: `repo` + `workflow`)
  - Dùng cho: GitHub Actions checkout & push (để trigger Pages deploy)
- Token client-side: Lưu trong `localStorage` (key: `gh_pat`)
  - Dùng cho: JS gọi GitHub API dispatch + poll status
- Push protection: Đã tắt cho repo (để workflow push commit có token)
- Repo là **private** → chỉ collaborator thấy code

### Khi có dữ liệu mới (KI-73):
1. Upload file Excel mới vào `data/TonKhoRo/` hoặc `data/Trip/` (qua GitHub UI hoặc git push)
2. Pipeline **tự chạy ngay** (trigger `push: data/**`)
3. KHÔNG cần chờ 2 tiếng, KHÔNG cần bấm nút, KHÔNG cần máy local

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

### Header Layout (KI-68, KI-71, KI-72)
- Header dùng `position: fixed` inline style (KI-71). Cố định góc trái trên.
- `.main-panel` scroll trong viewport: `max-height: calc(100vh - 40px); overflow-y: auto` (KI-72).
- `.container` có `height: calc(100vh - 16px); overflow: hidden`.
- Spacer div `width: 420px` trong mỗi panel tạo khoảng trống cho header.
- Token GitHub thiếu scope `workflow` → sửa `.github/workflows/` trực tiếp trên GitHub web (KI-69).

# Global Git Sync Rule
Whenever you modify project files, you MUST commit and push using the PAT token:
```powershell
git remote set-url origin "https://longdoanthanh-bot:<GH_PAT>@github.com/longdoanthanh-bot/dashboard-ro.git"
git add . && git commit -m "Your commit message"
git push origin master
git push origin master:main
git remote set-url origin "https://github.com/longdoanthanh-bot/dashboard-ro.git"
```
Push cả 2 nhánh: `master` và `master:main`. Restore URL sau khi push (xóa token khỏi remote).
