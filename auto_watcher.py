"""
Auto Watcher: Theo dõi thư mục G: Drive, tự động cập nhật Dashboard Rổ.
Khi phát hiện file JSON hoặc Excel thay đổi → chạy các script update → git commit + push.
"""
import os
import sys
import time
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

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Thư mục cần theo dõi
watch_dirs = {
    "master": (r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master", ".json"),
    "xnt": (r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Tồn kho Rổ", ".xlsx"),
    "trip": (r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Trip", ".xlsx")
}

# Loại bỏ GITHUB_TOKEN nếu bị conflict
if "GITHUB_TOKEN" in os.environ:
    del os.environ["GITHUB_TOKEN"]

def get_latest_state():
    """Lấy tổng hợp thời gian sửa đổi mới nhất của các file trong các thư mục."""
    state = []
    for key, (directory, ext) in watch_dirs.items():
        try:
            files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(ext) and not f.startswith("~$")]
            if files:
                state.append(str(max(os.path.getmtime(f) for f in files)))
            else:
                state.append("0")
        except Exception:
            state.append("0")
    return "_".join(state)

def git_push_auto():
    """Git add + commit + push lên cả master và main."""
    try:
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        commit_msg = f"Auto update {current_time}"
        print("  → Đang commit + push lên GitHub...")

        # Git pull first to avoid push rejection
        subprocess.run(
            ["git", "pull", "--rebase", "origin", "master"],
            cwd=PROJECT_DIR,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Git add
        subprocess.run(
            ["git", "add", "index.html", "tele.html", "tasks.html", "data.js", "sla_v5.html", "data/"],
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

        # Push master
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
    for k, (v, ext) in watch_dirs.items():
        print(f"Theo dõi [{ext}] tại: {v}")
    print("---------------------------------------------------------")

    last_state = get_latest_state()
    print(f"[{time.strftime('%X')}] Trạng thái ban đầu: {last_state}")

    # Chạy cập nhật 1 lần lúc khởi động nếu cần, nhưng tạm thời chỉ log
    # Nếu muốn tự động cập nhật ngay khi bật watcher thì bỏ comment:
    # print(f"[{time.strftime('%X')}] Đang cập nhật lần đầu...")
    # subprocess.run(["python", "update_store_data.py"], cwd=PROJECT_DIR)
    # subprocess.run(["python", "update_excel_data.py"], cwd=PROJECT_DIR)
    # git_push_auto()

    print(f"[{time.strftime('%X')}] Đang theo dõi... (Ctrl+C để dừng)")
    while True:
        try:
            time.sleep(3)  # Kiểm tra mỗi 3 giây
            current_state = get_latest_state()

            if current_state != last_state:
                print(f"\n[{time.strftime('%X')}] Phát hiện thay đổi dữ liệu!")
                
                # Gọi scripts update
                print("  → Cập nhật Store Data...")
                subprocess.run(["python", "update_store_data.py"], cwd=PROJECT_DIR)
                
                print("  → Cập nhật Excel Data...")
                subprocess.run(["python", "update_excel_data.py"], cwd=PROJECT_DIR)
                
                print("  → Cập nhật SLA Data...")
                subprocess.run(["python", "update_sla_data.py"], cwd=PROJECT_DIR)
                
                git_push_auto()
                last_state = current_state
                
        except KeyboardInterrupt:
            print(f"[{time.strftime('%X')}] Dừng theo dõi.")
            break
        except Exception as e:
            print(f"[{time.strftime('%X')}] Lỗi trong vòng lặp: {e}")
            time.sleep(10)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # Ghi crash log
        crash_log = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "watcher_crash.log"
        )
        with open(crash_log, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] CRASH: {e}\n")
            import traceback
            traceback.print_exc(file=f)
        raise
