"""
Auto Watcher: Theo dõi thư mục G: Drive, tự động cập nhật Dashboard Rổ.
Khi phát hiện file JSON thay đổi → inject vào index.html → git commit + push.
"""
import os
import sys
import time
import json
import re
import shutil
import subprocess
from datetime import datetime

# Fix pythonw (headless): stdout/stderr là None → redirect sang log file
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "watcher.log")
if sys.stdout is None or sys.stderr is None:
    _log_file = open(LOG_PATH, "a", encoding="utf-8", buffering=1)
    sys.stdout = _log_file
    sys.stderr = _log_file
else:
    os.environ["PYTHONIOENCODING"] = "utf-8"
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# KI-14: Đường dẫn tương đối từ vị trí script
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

watch_dir = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master"
html_path = os.path.join(PROJECT_DIR, "index.html")

# Loại bỏ GITHUB_TOKEN nếu bị conflict (KI-9: fix root cause)
if "GITHUB_TOKEN" in os.environ:
    del os.environ["GITHUB_TOKEN"]


def update_html_with_json(json_path):
    """Inject JSON data vào index.html + cập nhật timestamp."""
    print(f"[{time.strftime('%X')}] Đang xử lý: {os.path.basename(json_path)}")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            print("  → Lỗi: JSON không phải dictionary.")
            return False

        stores_list = list(data.values())
        stores_js = json.dumps(stores_list, ensure_ascii=False)

        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        pattern = re.compile(r'(const\s+STORE_COORDS\s*=\s*)\[.*?\];', re.DOTALL)
        if not pattern.search(html_content):
            print("  → Lỗi: Không tìm thấy biến STORE_COORDS trong index.html")
            return False

        new_html_content = pattern.sub(r'\g<1>' + stores_js + ';', html_content)

        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        pattern_time = re.compile(r'<div>Cập nhật:.*?</div>')
        new_html_content = pattern_time.sub(f'<div>Cập nhật: {current_time}</div>', new_html_content)

        # KI-3: Backup trước khi ghi đè
        backup_path = html_path + ".bak"
        try:
            shutil.copy2(html_path, backup_path)
        except Exception as e:
            print(f"  → Cảnh báo: Không tạo được backup: {e}")

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_html_content)

        print(f"  → OK: {len(stores_list)} cửa hàng + timestamp ({current_time})")
        return True
    except Exception as e:
        print(f"  → Lỗi xử lý: {e}")
        return False


def get_latest_json(directory):
    """Tìm file JSON mới nhất trong thư mục."""
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
    except Exception:
        pass
    return latest_file, latest_time


def git_push_auto():
    """Git add + commit + push lên cả master và main (KI-37)."""
    try:
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        commit_msg = f"Auto update {current_time}"
        print("  → Đang commit + push lên GitHub...")

        # Git add
        subprocess.run(
            ["git", "add", "index.html"],
            cwd=PROJECT_DIR, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Git commit
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=PROJECT_DIR, capture_output=True, text=True
        )
        if result.returncode != 0:
            print("  → Không có thay đổi mới để commit.")
            return

        # KI-37: Push cả master và main
        subprocess.run(
            ["git", "push", "origin", "master"],
            cwd=PROJECT_DIR, check=True
        )
        subprocess.run(
            ["git", "push", "origin", "master:main"],
            cwd=PROJECT_DIR,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print(f"  → THÀNH CÔNG: Dashboard sẽ cập nhật trong 1-2 phút.")
    except subprocess.CalledProcessError as e:
        print(f"  → LỖI KHI PUSH: {e}")
    except Exception as e:
        print(f"  → LỖI KHÔNG XÁC ĐỊNH: {e}")


def main():
    print("=========================================================")
    print("    AUTO UPDATE DASHBOARD - THEO DÕI THƯ MỤC G: DRIVE")
    print("=========================================================")
    print(f"Thư mục theo dõi : {watch_dir}")
    print(f"File HTML đích    : {html_path}")
    print(f"Git repo          : {PROJECT_DIR}")
    print("---------------------------------------------------------")

    last_processed_file = None
    last_processed_time = 0

    # Kiểm tra ban đầu
    latest_f, latest_t = get_latest_json(watch_dir)
    if latest_f:
        print(f"[{time.strftime('%X')}] File hiện tại: {os.path.basename(latest_f)}")
        last_processed_file = latest_f
        last_processed_time = latest_t

    # Vòng lặp theo dõi
    print(f"[{time.strftime('%X')}] Đang theo dõi... (Ctrl+C để dừng)")
    while True:
        try:
            time.sleep(3)  # Kiểm tra mỗi 3 giây
            latest_f, latest_t = get_latest_json(watch_dir)

            if latest_f and (latest_f != last_processed_file or latest_t > last_processed_time):
                print(f"\n[{time.strftime('%X')}] Phát hiện thay đổi dữ liệu!")
                success = update_html_with_json(latest_f)
                if success:
                    last_processed_file = latest_f
                    last_processed_time = latest_t
                    git_push_auto()
        except KeyboardInterrupt:
            print(f"[{time.strftime('%X')}] Dừng theo dõi.")
            break
        except Exception as e:
            print(f"[{time.strftime('%X')}] Lỗi trong vòng lặp: {e}")
            time.sleep(10)  # Chờ lâu hơn nếu có lỗi, tránh spam


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # Ghi crash log cho pythonw (headless)
        crash_log = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "watcher_crash.log"
        )
        with open(crash_log, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] CRASH: {e}\n")
            import traceback
            traceback.print_exc(file=f)
        raise
