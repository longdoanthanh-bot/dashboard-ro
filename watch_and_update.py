import sys
import time
import subprocess
import os
from threading import Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def run_hidden(*args, **kwargs):
    if os.name == 'nt':
        kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
    return subprocess.run(*args, **kwargs)

sys.stdout.reconfigure(encoding='utf-8')

# Đường dẫn cần theo dõi
WATCH_DIR = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source"
# Script cập nhật - ĐÃ SỬA LẠI ĐỂ KHÔNG PHỤ THUỘC Ổ D
UPDATE_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_update.bat")
# Thời gian chờ (debounce) sau khi file được tạo/lưu hoàn tất (5 giây)
DEBOUNCE_TIME = 5.0

class WatcherHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.timer = None

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        # Chỉ quan tâm đến file Excel (.xlsx)
        if event.is_directory or not event.src_path.endswith('.xlsx'):
            return
        
        # Bỏ qua file tạm của Excel mở (bắt đầu bằng ~$)
        filename = os.path.basename(event.src_path)
        if filename.startswith('~$'):
            return

        print(f"\n[PHÁT HIỆN] Thay đổi ở file: {event.src_path}")
        
        # Hủy timer cũ nếu có file liên tục được ghi
        if self.timer:
            self.timer.cancel()
        
        # Đặt lại timer mới
        self.timer = Timer(DEBOUNCE_TIME, self.run_update)
        self.timer.start()

    def run_update(self):
        print(f"\n[BẮT ĐẦU] Cập nhật số liệu...")
        try:
            # Lệnh chạy run_update.bat, thư mục gốc
            run_hidden([UPDATE_SCRIPT], cwd=os.path.dirname(UPDATE_SCRIPT), shell=True, check=True)
            print("[THÀNH CÔNG] Đã cập nhật xong và Push lên Github!")
        except subprocess.CalledProcessError as e:
            print(f"[LỖI] Cập nhật thất bại. Chi tiết: {e}")

if __name__ == "__main__":
    print("="*60)
    print("🚀 ĐANG THEO DÕI THƯ MỤC DATA_SOURCE...")
    print(f"📁 Thư mục: {WATCH_DIR}")
    print("="*60)
    
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[DỪNG] Ngừng theo dõi.")
        
    observer.join()
