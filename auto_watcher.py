import os
import time
import json
import re
import subprocess

watch_dir = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master"
html_path = r"G:\My Drive\ANTIGRAVITY\Tro_Ly\dashboard-ro\index.html"

def update_html_with_json(json_path):
    print(f"[{time.strftime('%X')}] Dang xu ly file: {os.path.basename(json_path)}")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Kiem tra xem co phai json chua danh sach ST khong
        if not isinstance(data, dict):
            return False
            
        stores_list = list(data.values())
        stores_js = json.dumps(stores_list, ensure_ascii=False)
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        pattern = re.compile(r'(const\s+STORE_COORDS\s*=\s*)\[.*?\];', re.DOTALL)
        if not pattern.search(html_content):
            print("-> Loi: Khong tim thay bien const STORE_COORDS trong html.")
            return False
            
        new_html_content = pattern.sub(r'\g<1>' + stores_js + ';', html_content)
        
        from datetime import datetime
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        pattern_time = re.compile(r'<div>Cập nhật:.*?</div>')
        new_html_content = pattern_time.sub(f'<div>Cập nhật: {current_time}</div>', new_html_content)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_html_content)
            
        print(f"-> Thanh cong! Da tu dong nạp {len(stores_list)} ST va thoi gian ({current_time}) len Dashboard.")
        return True
    except Exception as e:
        print(f"-> Loi xu ly: {e}")
        return False

def get_latest_json(directory):
    latest_file = None
    latest_time = 0
    try:
        for f in os.listdir(directory):
            if f.lower().endswith('.json'):
                full_path = os.path.join(directory, f)
                mtime = os.path.getmtime(full_path)
                if mtime > latest_time:
                    latest_time = mtime
                    latest_file = full_path
    except:
        pass
    return latest_file, latest_time

def git_push_auto():
    try:
        from datetime import datetime
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        commit_msg = f"Auto update {current_time}"
        print("-> Dang tien hanh push tu dong len GitHub...")
        cwd_path = r"G:\My Drive\ANTIGRAVITY\Tro_Ly\dashboard-ro"
        
        # Thêm file index.html
        subprocess.run(["git", "add", "index.html"], cwd=cwd_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Commit thay đổi
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=cwd_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Push lên GitHub
        subprocess.run(["git", "push", "origin", "master"], cwd=cwd_path, check=True)
        print("-> THÀNH CÔNG: Đã tự động cập nhật web trên GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"-> LỖI KHI PUSH LÊN GITHUB. Vui lòng kiểm tra lại quyền truy cập hoặc push tay. Lỗi: {e}")
    except Exception as e:
        print(f"-> LỖI KHÔNG XÁC ĐỊNH KHI PUSH: {e}")

def main():
    print("=========================================================")
    print("    AUTO UPDATE DASHBOARD THEO DOI THU MUC G: DRIVE")
    print("=========================================================")
    print(f"Thu muc: {watch_dir}")
    print("Huong dan: De cua so nay chay ngam (thu nho xuong). Bat cu khi nao")
    print("co file .json moi hoac duoc sua, du lieu se TU DONG update.")
    print("---------------------------------------------------------")
    
    last_processed_file = None
    last_processed_time = 0
    
    # Kiem tra ban dau
    latest_f, latest_t = get_latest_json(watch_dir)
    if latest_f:
        print(f"[{time.strftime('%X')}] Da tim thay file hien tai: {os.path.basename(latest_f)}")
        last_processed_file = latest_f
        last_processed_time = latest_t
        update_html_with_json(latest_f)

    # Vong lap vo han de theo doi
    while True:
        time.sleep(3) # Kiem tra moi 3 giay
        latest_f, latest_t = get_latest_json(watch_dir)
        
        # Neu co file moi, hoac file cu vua duoc cap nhat
        if latest_f and (latest_f != last_processed_file or latest_t > last_processed_time):
            print(f"[{time.strftime('%X')}] Phat hien thay doi du lieu!")
            success = update_html_with_json(latest_f)
            if success:
                last_processed_file = latest_f
                last_processed_time = latest_t
                
                # Gọi hàm push tự động
                git_push_auto()

if __name__ == '__main__':
    main()
