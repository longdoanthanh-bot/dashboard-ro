"""
Inject nút "Cập nhật" + Error Popup vào index.html
Nút gọi http://localhost:5588/update (update_server.py) để chạy pipeline.
KI-compliant: không xóa HTML markers.
"""
import os, sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(PROJECT_DIR, "index.html")

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. CSS — append before </style>
# ============================================================
UPDATE_CSS = """
/* === UPDATE BUTTON & POPUP === */
.btn-update {
    background: linear-gradient(135deg, #10b981, #34d399);
    border: none; color: #fff; padding: 6px 14px; border-radius: var(--radius);
    cursor: pointer; font-size: 12px; font-weight: 700; font-family: inherit;
    display: flex; align-items: center; gap: 6px; transition: all 0.25s;
    box-shadow: 0 2px 8px rgba(16,185,129,0.3); white-space: nowrap;
}
.btn-update:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(16,185,129,0.45); }
.btn-update:active { transform: scale(0.97); }
.btn-update.loading {
    opacity: 0.7; pointer-events: none;
    background: linear-gradient(135deg, #6b7280, #9ca3af);
    box-shadow: 0 2px 8px rgba(107,114,128,0.3);
}
.btn-update .spinner {
    display: none; width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.3);
    border-top-color: #fff; border-radius: 50%; animation: spin 0.6s linear infinite;
}
.btn-update.loading .spinner { display: inline-block; }
.btn-update.loading .btn-update-icon { display: none; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Popup overlay */
.popup-overlay {
    display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.6);
    backdrop-filter: blur(4px); z-index: 99999; align-items: center; justify-content: center;
}
.popup-overlay.active { display: flex; animation: fadeIn 0.2s; }
.popup-box {
    background: var(--card); border: 1px solid var(--border); border-radius: 16px;
    padding: 28px 32px; max-width: 520px; width: 90%; box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    animation: slideDown 0.25s ease;
}
.popup-box .popup-header { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
.popup-box .popup-icon { font-size: 28px; }
.popup-box .popup-title-text { font-size: 17px; font-weight: 700; color: var(--text); }
.popup-box .popup-msg {
    font-size: 13px; color: var(--text2); line-height: 1.7; white-space: pre-wrap;
    word-break: break-word; max-height: 350px; overflow-y: auto;
    background: var(--bg2); border-radius: 8px; padding: 12px 14px; border: 1px solid var(--border);
}
.popup-box .popup-actions { display: flex; gap: 8px; margin-top: 18px; justify-content: flex-end; }
.popup-box .popup-close-btn {
    background: var(--blue); border: none; color: #fff;
    padding: 8px 24px; border-radius: 8px; font-size: 13px; font-weight: 600;
    cursor: pointer; font-family: inherit; transition: all 0.2s;
}
.popup-box .popup-reload-btn {
    background: var(--green); border: none; color: #fff;
    padding: 8px 24px; border-radius: 8px; font-size: 13px; font-weight: 600;
    cursor: pointer; font-family: inherit; transition: all 0.2s; display: none;
}
.popup-box .popup-close-btn:hover, .popup-box .popup-reload-btn:hover { opacity: 0.85; }
.popup-box.popup-success .popup-title-text { color: var(--green); }
.popup-box.popup-error .popup-title-text { color: var(--red); }
.popup-box.popup-info .popup-title-text { color: var(--blue); }
"""

html = html.replace('</style>', UPDATE_CSS + '\n</style>', 1)

# ============================================================
# 2. HTML — add button next to theme toggle
# ============================================================
BUTTON_HTML = """        <button class="btn-update" id="btnUpdate" onclick="triggerUpdate()" title="Chạy pipeline cập nhật dữ liệu mới nhất">
            <span class="btn-update-icon">🔄</span><span class="spinner"></span> Cập nhật
        </button>"""

# Insert after the theme toggle button
theme_btn_end = '</button>\n        <div style="font-size:11px; color:var(--text3);" id="last-update-time">'
html = html.replace(
    theme_btn_end,
    '</button>\n' + BUTTON_HTML + '\n        <div style="font-size:11px; color:var(--text3);" id="last-update-time">',
    1
)

# Add popup before </body>
POPUP_HTML = """
<!-- UPDATE POPUP -->
<div class="popup-overlay" id="updatePopup" onclick="if(event.target===this)closeUpdatePopup()">
    <div class="popup-box" id="updatePopupBox">
        <div class="popup-header">
            <span class="popup-icon" id="popupIcon">✅</span>
            <span class="popup-title-text" id="popupTitle">Thông báo</span>
        </div>
        <div class="popup-msg" id="popupMsg"></div>
        <div class="popup-actions">
            <button class="popup-reload-btn" id="popupReloadBtn" onclick="location.reload()">🔄 Tải lại trang</button>
            <button class="popup-close-btn" onclick="closeUpdatePopup()">Đóng</button>
        </div>
    </div>
</div>
"""

html = html.replace('</body>', POPUP_HTML + '\n</body>', 1)

# ============================================================
# 3. JavaScript — add update trigger before </script>
# ============================================================
UPDATE_JS = """
// === LOCAL UPDATE TRIGGER ===
const UPDATE_SERVER = 'http://localhost:5588';

function showUpdatePopup(type, title, msg, showReload) {
    const overlay = document.getElementById('updatePopup');
    const box = document.getElementById('updatePopupBox');
    const icon = document.getElementById('popupIcon');
    const titleEl = document.getElementById('popupTitle');
    const msgEl = document.getElementById('popupMsg');
    const reloadBtn = document.getElementById('popupReloadBtn');
    
    box.className = 'popup-box popup-' + type;
    icon.textContent = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
    titleEl.textContent = title;
    msgEl.textContent = msg;
    reloadBtn.style.display = showReload ? 'inline-block' : 'none';
    overlay.classList.add('active');
}

function closeUpdatePopup() {
    document.getElementById('updatePopup').classList.remove('active');
}

async function triggerUpdate() {
    const btn = document.getElementById('btnUpdate');
    btn.classList.add('loading');
    
    try {
        // Check if server is running first
        try {
            const statusResp = await fetch(UPDATE_SERVER + '/status', { signal: AbortSignal.timeout(3000) });
            if (!statusResp.ok) throw new Error('Server not ok');
        } catch (e) {
            showUpdatePopup('error', 'Không kết nối được server',
                'Server cập nhật chưa chạy trên máy local.\\n\\n' +
                'Hãy mở Terminal/CMD tại thư mục dự án và chạy:\\n' +
                '  python update_server.py\\n\\n' +
                'Server sẽ lắng nghe tại http://localhost:5588\\n' +
                'Sau đó bấm "Cập nhật" lại.', false);
            btn.classList.remove('loading');
            return;
        }
        
        // Trigger update
        const resp = await fetch(UPDATE_SERVER + '/update', { signal: AbortSignal.timeout(180000) });
        const result = await resp.json();
        
        if (result.success) {
            let detail = result.message || 'Thành công!';
            if (result.steps && result.steps.length > 0) {
                detail += '\\n\\n📋 Chi tiết các bước:';
                for (const step of result.steps) {
                    detail += '\\n  ' + (step.ok ? '✅' : '❌') + ' ' + step.step;
                }
            }
            showUpdatePopup('success', 'Cập nhật thành công!', detail, true);
        } else {
            let detail = result.message || 'Có lỗi xảy ra';
            if (result.errors && result.errors.length > 0) {
                detail += '\\n\\n🔴 Lỗi chi tiết:';
                for (const err of result.errors) {
                    detail += '\\n  • ' + err;
                }
            }
            if (result.steps && result.steps.length > 0) {
                detail += '\\n\\n📋 Các bước đã chạy:';
                for (const step of result.steps) {
                    detail += '\\n  ' + (step.ok ? '✅' : '❌') + ' ' + step.step;
                }
            }
            showUpdatePopup('error', 'Cập nhật thất bại', detail, false);
        }
    } catch (err) {
        if (err.name === 'TimeoutError' || err.message?.includes('timeout')) {
            showUpdatePopup('error', 'Quá thời gian chờ',
                'Pipeline cập nhật chạy quá 3 phút.\\n' +
                'Kiểm tra terminal đang chạy update_server.py để xem chi tiết.', false);
        } else {
            showUpdatePopup('error', 'Lỗi kết nối',
                'Không thể kết nối đến server cập nhật.\\n\\n' +
                'Chi tiết: ' + (err.message || String(err)) + '\\n\\n' +
                'Đảm bảo update_server.py đang chạy trên máy local.', false);
        }
    } finally {
        btn.classList.remove('loading');
    }
}
"""

# Insert before the last </script>
last_script_pos = html.rfind('</script>')
if last_script_pos != -1:
    html = html[:last_script_pos] + UPDATE_JS + '\n' + html[last_script_pos:]

# ============================================================
# 4. Write back
# ============================================================
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"[OK] Injected update button + popup into index.html")
print(f"     File size: {os.path.getsize(html_path):,} bytes")
print(f"     Button calls http://localhost:5588/update")
print(f"     Run 'python update_server.py' to start the local server.")
