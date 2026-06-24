import json
import re
import os
import sys
import shutil
from datetime import datetime

# Fix Windows console encoding
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# KI-14: Đường dẫn tương đối từ vị trí script
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

json_path = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master\store_coordinates.json"
html_path = os.path.join(PROJECT_DIR, "index.html")

def main():
    # --- Kiểm tra file tồn tại ---
    if not os.path.exists(json_path):
        print(f"[LỖI] Không tìm thấy file JSON: {json_path}")
        sys.exit(1)

    if not os.path.exists(html_path):
        print(f"[LỖI] Không tìm thấy file HTML: {html_path}")
        sys.exit(1)

    # 1. Đọc dữ liệu từ file JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"[LỖI] Đọc file JSON thất bại: {e}")
            sys.exit(1)

    # 2. Chuyển dictionary thành list → chuỗi JSON
    stores_list = list(data.values())
    stores_js = json.dumps(stores_list, ensure_ascii=False)

    # 3. Đọc nội dung file index.html
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 4. Thay thế mảng STORE_COORDS bằng Regex
    pattern = re.compile(r'(const\s+STORE_COORDS\s*=\s*)\[.*?\];', re.DOTALL)

    if not pattern.search(html_content):
        print("[LỖI] Không tìm thấy biến 'const STORE_COORDS = [...];' trong index.html")
        sys.exit(1)

    new_html_content = pattern.sub(r'\g<1>' + stores_js + ';', html_content)

    # Cập nhật timestamp
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    pattern_time = re.compile(r'<div>Cập nhật:.*?</div>')
    new_html_content = pattern_time.sub(f'<div>Cập nhật: {current_time}</div>', new_html_content)

    # KI-3: Tạo backup trước khi ghi đè
    backup_path = html_path + ".bak"
    try:
        shutil.copy2(html_path, backup_path)
    except Exception as e:
        print(f"[CẢNH BÁO] Không tạo được backup: {e}")

    # 5. Ghi đè lại file index.html
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_html_content)
    except Exception as e:
        print(f"[LỖI] Ghi file HTML thất bại: {e}")
        # Khôi phục từ backup nếu có
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, html_path)
            print("[KHÔI PHỤC] Đã restore từ backup.")
        sys.exit(1)

    print(f"[OK] Đã cập nhật {len(stores_list)} cửa hàng + timestamp ({current_time}) vào index.html")
    sys.exit(0)

if __name__ == '__main__':
    main()
