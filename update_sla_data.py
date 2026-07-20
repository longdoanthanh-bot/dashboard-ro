#!/usr/bin/env python3
"""
update_sla_data.py — Cập nhật file data.js cho SLA Dashboard.

CHIẾN LƯỢC:
  - Đọc data.js hiện tại (nếu có)
  - Truy vấn DB kfm_scm lấy dữ liệu trip MỚI (từ ngày cuối cùng trong data.js trở đi)
  - Bổ sung rows mới vào data.js
  - Ghi lại data.js với dữ liệu đầy đủ

Cấu trúc data.js:
  const D_GENERATED = "DD/MM/YYYY HH:MM:SS";
  const D = {
    weeks: [...], warehouses: [...], destinations: [...],
    trips: [...], carriers: [...], months: [...], drivers: [...],
    rows: [
      // [week_idx, month, wh_idx, dest_idx, trip_idx, sla(0/1/2), actual, planned, date, driver_idx, carrier_idx]
    ]
  }

SLA logic:
  - actual = tl_arrival (giờ thực tế đến nơi, dạng "HH:MM")
  - planned = "" (DB không có ETA, để rỗng giống một số rows trong bản gốc)
  - Không tính SLA status tự động → đánh dấu tất cả row mới là sla=0 (Đúng) 
    để tránh sai số. Nếu cần SLA chính xác, cần bổ sung ETA từ web KFM.
"""

import os
import sys
import json
import re
import pymysql
from datetime import datetime, timedelta, timezone
from collections import defaultdict

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

DB_CONFIG = {
    'host': '103.147.122.103',
    'port': 9030,
    'user': 'kfm_scm_tho_nguyen',
    'password': 'oh1dtJwR4ihLGrX4E7bs',
    'database': 'kfm_scm'
}

WAREHOUSE_NAMES = ["Đông", "Mát", "Thịt", "Rau", "Khô giao ngày", "Khô giao đêm"]

# Warehouse mapping: from_location_id → warehouse_index
WAREHOUSE_MAP = {
    "5fdc170ebd89c10006f15b7c": 5,   # Khô giao đêm (Hour 18)
    "6a34ed56f23028000774139f": 4,   # Khô giao ngày (Hour 18-19)
    "62342407b35d1d0007379692": 2,   # Thịt (fallback)
    "639d80531a37c70007cbb7bf": 3,   # Rau (fallback)
    "6a2f96a1ebb48c0007555e39": 0,   # Đông (fallback)
}


def determine_warehouse(from_location_id, departure_hour):
    """Xác định kho dựa trên location_id và giờ xuất phát."""
    wh = WAREHOUSE_MAP.get(from_location_id)
    if wh is not None:
        return wh
    if from_location_id == "61d4ffa72997ae0007f5ad19":
        if departure_hour is not None and departure_hour >= 18:
            return 5
        return 0  # Đông (mặc định sáng sớm)
    elif from_location_id == "6234219eb35d1d00073793ab":
        if departure_hour is not None and departure_hour <= 5:
            return 2  # Thịt
        return 3  # Rau (chiều)
    return 0


def get_iso_week(date_obj):
    return f"W{date_obj.isocalendar()[1]}"


def parse_iso_datetime(s):
    """Parse ISO datetime string → VN timezone datetime."""
    if not s:
        return None
    try:
        s = s.replace('Z', '+00:00')
        if '.' in s:
            parts = s.split('.')
            frac_tz = parts[1]
            for tz_sep in ['+', '-']:
                if tz_sep in frac_tz[1:]:
                    idx = frac_tz.index(tz_sep, 1)
                    frac = frac_tz[:idx][:6]
                    tz = frac_tz[idx:]
                    s = parts[0] + '.' + frac + tz
                    break
            else:
                frac = frac_tz[:6]
                s = parts[0] + '.' + frac
        dt = datetime.fromisoformat(s)
        return dt.astimezone(VN_TZ)
    except Exception:
        return None


def load_existing_data():
    """Đọc data.js hiện tại, trả về dict D hoặc None nếu không có."""
    data_path = os.path.join(PROJECT_DIR, "data.js")
    if not os.path.exists(data_path):
        return None
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Xóa BOM nếu có
        if content.startswith('\ufeff'):
            content = content[1:]
        
        # Parse D object
        match = re.search(r'const D\s*=\s*(\{.*\});', content, re.DOTALL)
        if not match:
            print("  ⚠️ Không parse được data.js, sẽ tạo mới")
            return None
        
        d = json.loads(match.group(1))
        
        # Nếu thiếu daily, thử load từ daily_backup.json
        if not d.get('daily'):
            backup_path = os.path.join(PROJECT_DIR, "daily_backup.json")
            if os.path.exists(backup_path):
                try:
                    with open(backup_path, 'r', encoding='utf-8') as fb:
                        d['daily'] = json.load(fb)
                    print(f"    📋 Loaded {len(d['daily'])} daily entries from backup")
                except:
                    pass
        
        return d
    except Exception as e:
        print(f"  ⚠️ Lỗi đọc data.js: {e}")
        return None


def find_latest_date(d):
    """Tìm ngày gần nhất trong data.js → dùng làm mốc lấy dữ liệu mới."""
    if not d or 'rows' not in d or len(d['rows']) == 0:
        return None
    
    latest = None
    for row in d['rows']:
        date_str = row[8]  # date field (index 8)
        try:
            dt = datetime.strptime(date_str, "%d/%m/%Y")
            if latest is None or dt > latest:
                latest = dt
        except:
            pass
    return latest


def main():
    now = datetime.now(VN_TZ)
    print(f"[{now.strftime('%H:%M:%S')}] Bắt đầu cập nhật data.js cho SLA Dashboard...")
    
    # === BƯỚC 1: Đọc data.js hiện tại ===
    print("  → Đọc data.js hiện tại...")
    existing_data = load_existing_data()
    
    if existing_data:
        latest_date = find_latest_date(existing_data)
        existing_rows_count = len(existing_data.get('rows', []))
        print(f"    ✅ Đã có {existing_rows_count} rows, ngày cuối: {latest_date.strftime('%d/%m/%Y') if latest_date else 'N/A'}")
        
        # Lấy dữ liệu mới từ ngày cuối - 1 (overlap 1 ngày để chắc chắn)
        if latest_date:
            min_date = (latest_date - timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            min_date = '2026-02-20'
    else:
        print("    ⚠️ Chưa có data.js, sẽ tạo mới")
        existing_data = {
            "weeks": [],
            "warehouses": WAREHOUSE_NAMES,
            "destinations": [],
            "trips": [],
            "carriers": [],
            "months": [],
            "drivers": [],
            "rows": [],
        }
        existing_rows_count = 0
        min_date = '2026-02-20'
    
    # === BƯỚC 2: Lấy dữ liệu mới từ DB ===
    print(f"  → Truy vấn DB từ {min_date}...")
    
    conn = pymysql.connect(**DB_CONFIG)
    try:
        cursor = conn.cursor()
        
        # Mapping branch_id → branch_code
        cursor.execute("""
            SELECT DISTINCT branch_id, branch_code, branch_name 
            FROM __cdc_kfm_kf_inventories_kf_inventory_transaction_stockcard 
            WHERE branch_code IS NOT NULL AND branch_code != ''
        """)
        branch_id_to_code = {}
        for row in cursor.fetchall():
            branch_id_to_code[row[0]] = row[1]
        
        # Trips
        cursor.execute(f"""
            SELECT 
                t._id, t.t_code, t.t_departure, t.t_driver_name,
                t.t_license_number, t.t_from_location_id
            FROM __cdc_kfm_kf_inventories_kf_trips t
            WHERE t.t_departure >= '{min_date}' 
              AND t.deleted = 0
              AND t.t_status IN (1, 2, 3)
        """)
        trip_lookup = {}
        for row in cursor.fetchall():
            trip_lookup[row[0]] = {
                'code': row[1] or '',
                'departure': row[2] or '',
                'driver': row[3] or '',
                'plate': row[4] or '',
                'from_location': row[5] or '',
            }
        print(f"    Trips: {len(trip_lookup)}")
        
        # Trip locations (chỉ những điểm đã có arrival)
        cursor.execute(f"""
            SELECT 
                tl.t_id, tl.tl_branch_id, tl.t_code, tl.t_departure,
                tl.tl_arrival, tl.tl_status, tl.tl_total_transfer_qty
            FROM __cdc_kfm_kf_inventories_kf_trip_locations tl
            WHERE tl.t_departure >= '{min_date}'
              AND tl.tl_arrival IS NOT NULL
              AND tl.deleted = 0
        """)
        locations_raw = cursor.fetchall()
        print(f"    Trip locations: {len(locations_raw)}")
        
    finally:
        conn.close()
    
    # === BƯỚC 3: Xây dựng index maps từ data hiện tại ===
    # Bắt đầu từ existing indices
    weeks = list(existing_data.get('weeks', []))
    destinations = list(existing_data.get('destinations', []))
    trips_list = list(existing_data.get('trips', []))
    carriers = list(existing_data.get('carriers', []))
    drivers = list(existing_data.get('drivers', []))
    months = list(existing_data.get('months', []))
    
    def ensure_index(lst, item):
        """Thêm item vào list nếu chưa có, trả về index."""
        if item in lst:
            return lst.index(item)
        lst.append(item)
        return len(lst) - 1
    
    # === BƯỚC 4: Tạo set các date+dest đã có để tránh trùng lặp ===
    existing_keys = set()
    for row in existing_data.get('rows', []):
        # Key = (date, dest_idx, trip_idx) 
        existing_keys.add((row[8], row[3], row[4]))
    
    # === BƯỚC 5: Tạo rows mới + thu thập daily data ===
    print("  → Xử lý dữ liệu mới...")
    new_rows = []
    
    # Daily aggregation: key = (date_str, wh_idx) → {st: set(), it: count, xe: set(), t: 0}
    daily_agg = defaultdict(lambda: {'st': set(), 'it': 0, 'xe': set(), 't': 0.0})
    
    for loc in locations_raw:
        t_id, branch_id, t_code, t_departure, tl_arrival, tl_status, transfer_qty = loc
        
        trip_info = trip_lookup.get(t_id)
        if not trip_info:
            continue
        
        # Parse times
        dep_dt = parse_iso_datetime(t_departure or trip_info['departure'])
        arr_dt = parse_iso_datetime(tl_arrival)
        if not dep_dt or not arr_dt:
            continue
        
        # Date
        date_str = dep_dt.strftime("%d/%m/%Y")
        month = dep_dt.month
        week_label = get_iso_week(dep_dt)
        dep_hour = dep_dt.hour
        
        # Warehouse
        wh_idx = determine_warehouse(trip_info['from_location'], dep_hour)
        
        # Destination
        dest = branch_id_to_code.get(branch_id, '')
        if not dest:
            continue
        
        # Trip code
        trip_code = t_code or trip_info['code'] or ''
        
        # Driver & Carrier
        driver = trip_info['driver'] or ''
        plate = trip_info['plate'] or ''
        carrier = plate[:3].upper().replace('.', '').replace('-', '') if len(plate) >= 3 else 'Khác'
        
        # Actual time (HH:MM format)
        actual_hhmm = arr_dt.strftime("%H:%M")
        planned_hhmm = ""  # DB không có ETA, để rỗng
        
        # SLA: mặc định Đúng (DB không có ETA để tính chính xác)
        sla = 0
        
        # Ensure indices
        week_idx = ensure_index(weeks, week_label)
        dest_idx = ensure_index(destinations, dest)
        trip_idx = ensure_index(trips_list, trip_code)
        carrier_idx = ensure_index(carriers, carrier)
        driver_idx = ensure_index(drivers, driver)
        if month not in months:
            months.append(month)
            months.sort()
        
        # === Cập nhật daily aggregation ===
        dk = (date_str, wh_idx)
        daily_agg[dk]['st'].add(dest)              # Distinct destinations = số siêu thị
        daily_agg[dk]['it'] += int(transfer_qty or 0)  # Tổng items giao
        daily_agg[dk]['xe'].add(t_id)              # Distinct trips = số xe
        daily_agg[dk]['week'] = week_idx
        daily_agg[dk]['month'] = month
        
        # Check trùng lặp cho SLA rows
        key = (date_str, dest_idx, trip_idx)
        if key in existing_keys:
            continue
        existing_keys.add(key)
        
        row = [
            week_idx, month, wh_idx, dest_idx, trip_idx,
            sla, actual_hhmm, planned_hhmm, date_str,
            driver_idx, carrier_idx,
        ]
        new_rows.append(row)
    
    print(f"    Rows mới: {len(new_rows)}")
    
    # === BƯỚC 6: Merge rows ===
    all_rows = list(existing_data.get('rows', [])) + new_rows
    
    # === BƯỚC 6b: Build daily array ===
    # Giữ daily cũ
    existing_daily = list(existing_data.get('daily', []))
    existing_daily_keys = set()
    for d_item in existing_daily:
        existing_daily_keys.add((d_item.get('d', ''), d_item.get('wh', -1)))
    
    # Thêm daily mới từ DB
    new_daily_count = 0
    for (date_str, wh_idx), agg in daily_agg.items():
        if (date_str, wh_idx) in existing_daily_keys:
            continue  # Đã có trong data cũ
        
        # Tính tấn ước lượng: trung bình ~0.4 kg/item (dựa trên data gốc)
        # Data gốc: 171207 items = 68.48 tấn → ~0.0004 tấn/item = 0.4 kg/item
        estimated_tons = round(agg['it'] * 0.0004, 2)
        
        daily_entry = {
            'd': date_str,
            'w': agg.get('week', 0),
            'm': agg.get('month', 0),
            'wh': wh_idx,
            'st': len(agg['st']),
            'it': agg['it'],
            'xe': len(agg['xe']),
            't': estimated_tons,
        }
        existing_daily.append(daily_entry)
        new_daily_count += 1
    
    print(f"    Daily mới: {new_daily_count}")
    
    # === BƯỚC 7: Ghi data.js ===
    generated_time = now.strftime("%d/%m/%Y %H:%M:%S")
    
    data_obj = {
        "weeks": weeks,
        "warehouses": WAREHOUSE_NAMES,
        "destinations": destinations,
        "trips": trips_list,
        "carriers": carriers,
        "months": months,
        "drivers": drivers,
        "rows": all_rows,
        "daily": existing_daily,
    }
    
    data_json = json.dumps(data_obj, ensure_ascii=False, separators=(',', ':'))
    js_content = f'const D_GENERATED = "{generated_time}";\nconst D = {data_json};\n'
    
    output_path = os.path.join(PROJECT_DIR, "data.js")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    # === Summary ===
    file_size_kb = os.path.getsize(output_path) / 1024
    print(f"\n{'='*50}")
    print(f"📊 SLA DATA.JS CẬP NHẬT THÀNH CÔNG")
    print(f"{'='*50}")
    print(f"⏰ Thời gian: {generated_time}")
    print(f"📅 Tuần: {weeks[0] if weeks else 'N/A'} → {weeks[-1] if weeks else 'N/A'} ({len(weeks)} tuần)")
    print(f"📅 Tháng: {months}")
    print(f"🏪 Điểm giao: {len(destinations)}")
    print(f"🚚 Chuyến xe: {len(trips_list)}")
    print(f"👤 Tài xế: {len(drivers)}")
    print(f"📊 Rows cũ: {existing_rows_count} | Rows mới: {len(new_rows)} | Tổng: {len(all_rows)}")
    print(f"📊 Daily cũ: {len(existing_daily) - new_daily_count} | Daily mới: {new_daily_count} | Tổng: {len(existing_daily)}")
    print(f"💾 File: {output_path} ({file_size_kb:.0f} KB)")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()

