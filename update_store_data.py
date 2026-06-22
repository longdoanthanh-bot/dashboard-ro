import json
import re
import os

json_path = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master\store_coordinates.json"
html_path = r"d:\LONG\LEARNING\ANTIGRAVITY\dashboard-ro\index.html"

def main():
    if not os.path.exists(json_path):
        print(f"Lỗi: Không tìm thấy file JSON tại {json_path}")
        return
    
    if not os.path.exists(html_path):
        print(f"Lỗi: Không tìm thấy file HTML tại {html_path}")
        return

    # 1. Đọc dữ liệu từ file JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Lỗi khi đọc file JSON: {e}")
            return
    
    # 2. Chuyển dictionary thành list
    # JSON có dạng: {"A196": {"code": "A196", ...}, "A182": {...}}
    stores_list = list(data.values())
    
    # Chuyển list thành chuỗi JSON JS
    stores_js = json.dumps(stores_list, ensure_ascii=False)
    
    # 3. Đọc nội dung file index.html
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    # 4. Thay thế mảng STORE_COORDS bằng Regex
    # Tìm kiếm đoạn: const STORE_COORDS = [...];
    pattern = re.compile(r'(const\s+STORE_COORDS\s*=\s*)\[.*?\];', re.DOTALL)
    
    # Kiểm tra xem có tìm thấy biến không
    if not pattern.search(html_content):
        print("Lỗi: Không tìm thấy biến 'const STORE_COORDS = [...];' trong file index.html")
        return
        
    new_html_content = pattern.sub(r'\g<1>' + stores_js + ';', html_content)
    
    from datetime import datetime
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    pattern_time = re.compile(r'<div>Cập nhật:.*?</div>')
    new_html_content = pattern_time.sub(f'<div>Cập nhật: {current_time}</div>', new_html_content)
    
    # 5. Ghi đè lại file index.html
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html_content)
        
    print(f"Thanh cong! Da cap nhat {len(stores_list)} cua hang va thoi gian ({current_time}) vao file index.html.")

if __name__ == '__main__':
    main()
