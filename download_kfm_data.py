#!/usr/bin/env python3
"""
Download KFM Data: Tự động tải file XNT (tồn kho rổ) và Trip từ next.kingfood.co
Dùng Playwright (headless Chromium) để login, filter, export Excel.

Env vars:
  KFM_USER - username đăng nhập
  KFM_PASS - password đăng nhập
  DATA_DIR - thư mục data (default: ./data)
"""
import os
import sys
import glob
import time
import re
from datetime import datetime, timezone, timedelta

# Fix encoding
os.environ["PYTHONIOENCODING"] = "utf-8"
try:
    if sys.stdout and sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VN_TZ = timezone(timedelta(hours=7))

KFM_USER = os.environ.get('KFM_USER', '')
KFM_PASS = os.environ.get('KFM_PASS', '')
DATA_DIR = os.environ.get('DATA_DIR', os.path.join(PROJECT_DIR, 'data'))

XNT_DIR = os.path.join(DATA_DIR, 'TonKhoRo')
TRIP_DIR = os.path.join(DATA_DIR, 'Trip')
DOWNLOAD_DIR = os.path.join(PROJECT_DIR, '_downloads')

# URLs
LOGIN_URL = "https://next.kingfood.co"
XNT_URL = "https://next.kingfood.co/stock/report-inventory-transaction"
TRIP_URL = "https://next.kingfood.co/operation/transfer-item/trip-list"

# Filter config for XNT
XNT_SAN_PHAM = [
    "Tote đỏ bánh tươi",
    "Rổ ABA đông mát",
    "Tote ABA đông mát",
    "Rổ cam xếp chồng quai đỏ",
    "Rổ nhựa đỏ kích thước 60x40x24 cm",
    "Rổ đen xếp chồng quai đỏ",
    "ITL Thùng tote xanh dương đục lỗ",
    "Seedlog - Thùng tote xanh lá, xanh dương không đục lỗ",
    "Rổ nhựa đen/xanh lá kho rau",
    "TOTE RỔ ĐEN CÓ NẮP",
]


def log(msg):
    now = datetime.now(VN_TZ).strftime("%H:%M:%S")
    print(f"[{now}] {msg}")


def login(page):
    """Login vào next.kingfood.co"""
    log("🔑 Đăng nhập vào KFM...")
    page.goto(LOGIN_URL, wait_until="networkidle", timeout=60000)
    time.sleep(2)
    
    # Check if already logged in
    if "/stock/" in page.url or "/operation/" in page.url or "/dashboard" in page.url:
        log("  ✅ Đã đăng nhập sẵn")
        return True
    
    # Find and fill login form
    try:
        username_sel = page.locator('input[type="text"], input[name="username"], input[name="email"], input[placeholder*="user" i], input[placeholder*="tên" i], input[placeholder*="email" i]').first
        password_sel = page.locator('input[type="password"]').first
        
        username_sel.fill(KFM_USER)
        time.sleep(0.5)
        password_sel.fill(KFM_PASS)
        time.sleep(0.5)
        
        login_btn = page.locator('button[type="submit"], button:has-text("Đăng nhập"), button:has-text("Login"), button:has-text("Sign in")').first
        login_btn.click()
        
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(3)
        
        if "login" in page.url.lower():
            log("  ❌ Đăng nhập thất bại")
            return False
        
        log("  ✅ Đăng nhập thành công")
        return True
        
    except Exception as e:
        log(f"  ❌ Lỗi đăng nhập: {e}")
        return False


def download_xnt(page):
    """Download XNT (tồn kho rổ) data."""
    today = datetime.now(VN_TZ)
    today_str = today.strftime("%d%m%Y")
    
    log(f"\n📦 TẢI TỒN KHO RỔ — {today.strftime('%d/%m/%Y')}")
    
    log("  Mở trang Xuất nhập tồn...")
    page.goto(XNT_URL, wait_until="networkidle", timeout=60000)
    time.sleep(3)
    
    # Open filter panel
    try:
        filter_icon = page.locator('[data-icon="filter"], button:has-text("Bộ lọc")').first
        if filter_icon.is_visible():
            filter_icon.click()
            time.sleep(1)
    except:
        pass
    
    # Select "tồn rổ" from first dropdown
    log("  Chọn 'tồn rổ'...")
    try:
        first_select = page.locator('.ant-select').first
        first_select.click()
        time.sleep(1)
        page.keyboard.type("tồn rổ")
        time.sleep(1)
        option = page.locator('.ant-select-item:has-text("tồn rổ"), .rc-virtual-list div:has-text("tồn rổ")').first
        if option.is_visible():
            option.click()
        else:
            page.keyboard.press("Enter")
        time.sleep(2)
    except Exception as e:
        log(f"  ⚠️ Chọn 'tồn rổ': {e}")
    
    # Click "Áp dụng"
    log("  Áp dụng filter...")
    try:
        apply_btn = page.locator('button:has-text("Áp dụng")').first
        apply_btn.click()
        time.sleep(5)
    except Exception as e:
        log(f"  ⚠️ Áp dụng: {e}")
    
    page.wait_for_load_state("networkidle", timeout=60000)
    time.sleep(2)
    
    # Click "Xuất báo cáo"
    log("  Xuất báo cáo...")
    try:
        with page.expect_download(timeout=120000) as download_info:
            export_btn = page.locator('button:has-text("Xuất báo cáo")').first
            export_btn.click()
        
        download = download_info.value
        filename = f"XNT_{today_str}.xlsx"
        
        os.makedirs(XNT_DIR, exist_ok=True)
        dest_path = os.path.join(XNT_DIR, filename)
        download.save_as(dest_path)
        
        size_kb = os.path.getsize(dest_path) / 1024
        log(f"  ✅ Đã tải: {filename} ({size_kb:.0f} KB)")
        return dest_path
        
    except Exception as e:
        log(f"  ❌ Lỗi xuất: {e}")
        return None


def download_trip(page):
    """Download Trip data."""
    today = datetime.now(VN_TZ)
    from_date = today - timedelta(days=5)
    
    log(f"\n🚛 TẢI TRIP — {from_date.strftime('%d/%m/%Y')} → {today.strftime('%d/%m/%Y')}")
    
    log("  Mở trang Trip list...")
    page.goto(TRIP_URL, wait_until="networkidle", timeout=60000)
    time.sleep(3)
    
    # Switch to "DS chuyến xe" tab
    log("  Chuyển tab 'DS chuyến xe'...")
    try:
        tab = page.locator('text="DS chuyến xe"').first
        if tab.is_visible():
            tab.click()
            time.sleep(2)
    except Exception as e:
        log(f"  ⚠️ Chuyển tab: {e}")
    
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(2)
    
    # Click "Xuất file"
    log("  Xuất file...")
    try:
        with page.expect_download(timeout=120000) as download_info:
            export_btn = page.locator('button:has-text("Xuất file")').first
            export_btn.click()
        
        download = download_info.value
        now_str = today.strftime("%d%m%Y-%H%M")
        filename = download.suggested_filename or f"DS-chi-tiet-chuyen-xe_{now_str}.xlsx"
        
        os.makedirs(TRIP_DIR, exist_ok=True)
        dest_path = os.path.join(TRIP_DIR, filename)
        download.save_as(dest_path)
        
        size_kb = os.path.getsize(dest_path) / 1024
        log(f"  ✅ Đã tải: {filename} ({size_kb:.0f} KB)")
        return dest_path
        
    except Exception as e:
        log(f"  ❌ Lỗi xuất: {e}")
        return None


def main():
    if not KFM_USER or not KFM_PASS:
        log("⚠️ Thiếu KFM_USER/KFM_PASS. Dùng dữ liệu hiện có.")
        return
    
    log("=" * 50)
    log("🚀 TẢI DỮ LIỆU TỪ KFM")
    log("=" * 50)
    
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            accept_downloads=True,
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        
        try:
            if not login(page):
                log("❌ Không thể đăng nhập. Dùng dữ liệu cũ.")
                return
            
            xnt_file = download_xnt(page)
            trip_file = download_trip(page)
            
            log(f"\n{'=' * 50}")
            log("📊 KẾT QUẢ:")
            log(f"  XNT: {'✅ ' + os.path.basename(xnt_file) if xnt_file else '❌ Thất bại'}")
            log(f"  Trip: {'✅ ' + os.path.basename(trip_file) if trip_file else '❌ Thất bại'}")
            log(f"{'=' * 50}")
            
        except Exception as e:
            log(f"❌ Lỗi: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()


if __name__ == "__main__":
    main()
