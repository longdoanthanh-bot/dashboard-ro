"""
Local Update Server — chạy trên localhost:5588
Dashboard (GitHub Pages) gọi endpoint này để trigger cập nhật dữ liệu.
"""
import os
import sys
import subprocess
import json
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from threading import Thread

# Fix encoding
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.stdout and sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 5588

# Loại bỏ GITHUB_TOKEN
if "GITHUB_TOKEN" in os.environ:
    del os.environ["GITHUB_TOKEN"]


def run_pipeline():
    """Chạy toàn bộ pipeline update + git push. Trả về dict kết quả."""
    steps = []
    errors = []

    def run_step(name, cmd, cwd=PROJECT_DIR):
        try:
            result = subprocess.run(
                cmd, cwd=cwd, capture_output=True, text=True, timeout=120,
                encoding='utf-8', errors='replace'
            )
            output = (result.stdout or '') + (result.stderr or '')
            ok = result.returncode == 0
            steps.append({"step": name, "ok": ok, "output": output.strip()[-500:]})
            if not ok:
                errors.append(f"[{name}] Exit code {result.returncode}: {output.strip()[-300:]}")
            return ok
        except subprocess.TimeoutExpired:
            steps.append({"step": name, "ok": False, "output": "TIMEOUT (>120s)"})
            errors.append(f"[{name}] Quá thời gian chờ (>120s)")
            return False
        except Exception as e:
            steps.append({"step": name, "ok": False, "output": str(e)})
            errors.append(f"[{name}] {str(e)}")
            return False

    # Step 0: Check khu vực (optional, skip if fails)
    run_step("check_khuvuc", [sys.executable, "check_khuvuc.py"])
    run_step("check_st", [sys.executable, "check_st.py"])

    # Step 1: Update store data
    if not run_step("update_store_data", [sys.executable, "update_store_data.py"]):
        return {"success": False, "steps": steps, "errors": errors, "message": "Lỗi cập nhật Store Data"}

    # Step 2: Update excel data
    if not run_step("update_excel_data", [sys.executable, "update_excel_data.py"]):
        return {"success": False, "steps": steps, "errors": errors, "message": "Lỗi cập nhật Excel Data"}

    # Step 3: Git add
    if not run_step("git_add", ["git", "add", "index.html", "tele.html", "tasks.html"]):
        return {"success": False, "steps": steps, "errors": errors, "message": "Lỗi git add"}

    # Step 4: Git commit
    ts = datetime.now().strftime("%d/%m/%Y %H:%M")
    commit_result = run_step("git_commit", ["git", "commit", "-m", f"Auto update {ts}"])
    if not commit_result:
        # Có thể không có gì thay đổi → coi như thành công
        last_step = steps[-1]
        if "nothing to commit" in last_step.get("output", "").lower():
            return {"success": True, "steps": steps, "errors": [], "message": "Dữ liệu không có thay đổi mới"}
        return {"success": False, "steps": steps, "errors": errors, "message": "Lỗi git commit"}

    # Step 5: Git push master
    if not run_step("git_push_master", ["git", "push", "origin", "master"]):
        return {"success": False, "steps": steps, "errors": errors, "message": "Lỗi git push master"}

    # Step 6: Git push master:main (optional)
    run_step("git_push_main", ["git", "push", "origin", "master:main"])

    return {
        "success": True,
        "steps": steps,
        "errors": [],
        "message": f"Cập nhật thành công! Dashboard sẽ live trong 1-2 phút.\nThời gian: {ts}"
    }


class UpdateHandler(BaseHTTPRequestHandler):
    def _set_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors()
        self.end_headers()

    def do_GET(self):
        if self.path == '/update':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self._set_cors()
            self.end_headers()

            print(f"[{datetime.now().strftime('%H:%M:%S')}] Bắt đầu cập nhật...")
            try:
                result = run_pipeline()
            except Exception as e:
                result = {
                    "success": False,
                    "steps": [],
                    "errors": [traceback.format_exc()],
                    "message": f"Lỗi nghiêm trọng: {str(e)}"
                }

            status = "THÀNH CÔNG" if result["success"] else "THẤT BẠI"
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Kết quả: {status} — {result['message']}")

            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))

        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self._set_cors()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "running", "port": PORT}).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress default access logs
        pass


def main():
    print("=" * 56)
    print("  DASHBOARD RỔ — LOCAL UPDATE SERVER")
    print(f"  Listening on http://localhost:{PORT}")
    print("=" * 56)
    print(f"  Project: {PROJECT_DIR}")
    print(f"  Endpoint: http://localhost:{PORT}/update")
    print(f"  Status:   http://localhost:{PORT}/status")
    print("-" * 56)
    print("  Dashboard sẽ gọi server này khi bấm nút Cập nhật.")
    print("  Ctrl+C để dừng.\n")

    server = HTTPServer(('127.0.0.1', PORT), UpdateHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Dừng server]")
        server.server_close()


if __name__ == '__main__':
    main()
