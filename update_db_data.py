import os
import re
import json
import shutil
import pymysql
from datetime import datetime, timedelta

# Fix Windows console encoding
os.environ["PYTHONIOENCODING"] = "utf-8"
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(PROJECT_DIR, "index.html")

DB_CONFIG = {
    'host': '103.147.122.103',
    'port': 9030,
    'user': 'kfm_scm_tho_nguyen',
    'password': 'oh1dtJwR4ihLGrX4E7bs',
    'database': 'kfm_scm'
}

XNT_MAPPING = {
    "ITL Thùng tote xanh dương đục lỗ": {"col": 0, "wh": "Dòng Mát"},
    "Rổ nhựa đen/xanh lá kho rau": {"col": 1, "wh": "Rau"},
    "Seedlog - Thùng tote xanh lá, xanh dương không đục lỗ": {"col": 2, "wh": "Khô"},
    "Rổ đen xếp chồng quai đỏ": {"col": 3, "wh": "Rau"},
    "Rổ nhựa đỏ kích thước 60x40x24 cm": {"col": 4, "wh": "Dòng Mát"},
    "Rổ cam xếp chồng quai đỏ (sóng nhựa hở BPGST-25V KT: 600x400x250)": {"col": 5, "wh": ""},
    "Rổ ABA đông mát": {"col": 6, "wh": "Dòng Mát"},
    "Tote ABA đông mát": {"col": 7, "wh": "Dòng Mát"},
    "Tote đỏ bánh tươi": {"col": 8, "wh": "Rau"},
    "TOTE RỔ ĐEN CÓ NẮP": {"col": 9, "wh": "Thịt Cá SCF"}
}

COUNTABLE_TRIP_CODES = {"B0001", "B0016", "B0015", "B0012", "B0017", "CC00392"}

def generate_tonkho_html(store_data, name_to_abbr):
    html_rows = []
    idx = 1
    sorted_stores = sorted(store_data.items(), key=lambda x: sum(x[1].values()), reverse=True)
    
    for st_name, cols in sorted_stores:
        abbr = name_to_abbr.get(st_name, "")
        total_sum = sum(cols.values())
        
        if total_sum > 60:
            tr_class = "tk-red"
        elif total_sum >= 50:
            tr_class = "tk-orange"
        elif total_sum >= 30:
            tr_class = "tk-yellow"
        else:
            tr_class = "tk-green"
            
        row_html = f'<tr class="{tr_class}"><td>{idx}</td><td class="st-code">{abbr}</td><td class="store-name">{st_name}</td><td class="num total-col">{total_sum}</td>'
        
        for col_idx in range(0, 10):
            val = cols.get(col_idx, 0)
            wh = ""
            for v in XNT_MAPPING.values():
                if v["col"] == col_idx:
                    wh = v["wh"]
                    break
                    
            classes = ["num", "bc-col"]
            if val == 0:
                classes.append("zero")
            elif val > 0:
                classes.append("high")
                
            row_html += f'<td class="{" ".join(classes)}" data-col="{col_idx}" data-warehouse="{wh}">{val}</td>'
            
        row_html += "</tr>"
        html_rows.append(row_html)
        idx += 1
        
    return "\n".join(html_rows)

def main():
    print(f"[{datetime.now()}] Bắt đầu update data từ DB...")
    
    # 1. Đọc STORE_COORDS từ index.html
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    match = re.search(r'const STORE_COORDS\s*=\s*(\[.*?\]);', html_content, re.DOTALL)
    if not match:
        print("Could not find STORE_COORDS in index.html")
        sys.exit(1)
        
    store_coords = json.loads(match.group(1))
    abbr_to_name = {s["abbr"]: s["name"] for s in store_coords if "name" in s and "abbr" in s}
    name_to_abbr = {s["name"]: s["abbr"] for s in store_coords if "name" in s and "abbr" in s}

    conn = pymysql.connect(**DB_CONFIG)
    
    try:
        with conn.cursor() as cursor:
            # 2. Xây dựng Mapping
            print("Đang tải mapping Cửa hàng & Sản phẩm...")
            cursor.execute("SELECT DISTINCT branch_id, branch_code FROM __cdc_kfm_kf_inventories_kf_inventory_transaction_stockcard WHERE branch_code IS NOT NULL AND branch_code != ''")
            branch_id_to_abbr = {row[0]: row[1] for row in cursor.fetchall()}
            
            cursor.execute("SELECT DISTINCT barcode, product_name FROM __cdc_kfm_kf_inventories_kf_inventory_transaction_stockcard WHERE product_name IS NOT NULL")
            barcode_to_product_name = {row[0]: row[1] for row in cursor.fetchall()}

            # 3. Lấy dữ liệu Tồn Kho (Stock) tối ưu
            print("Đang tải dữ liệu Tồn kho...")
            store_stock_data = {}
            target_barcodes = [bc for bc, name in barcode_to_product_name.items() if name in XNT_MAPPING]
            
            if target_barcodes:
                format_strings = ','.join(['%s'] * len(target_barcodes))
                q_stock = f"""
                SELECT branch_id, barcode, closing_stock
                FROM (
                    SELECT branch_id, barcode, closing_stock,
                           ROW_NUMBER() OVER(PARTITION BY branch_id, barcode ORDER BY updated_at DESC) as rn
                    FROM __cdc_kfm_kf_inventories_kf_inventory_transaction_stock_summaries
                    WHERE barcode IN ({format_strings})
                ) t
                WHERE t.rn = 1 AND t.closing_stock > 0
                """
                cursor.execute(q_stock, tuple(target_barcodes))
                
                for row in cursor.fetchall():
                    b_id, barcode, closing = row
                    if closing is None: continue
                    closing = int(closing)
                    
                    p_name = barcode_to_product_name.get(barcode, "")
                    if p_name in XNT_MAPPING:
                        abbr = branch_id_to_abbr.get(b_id)
                        if abbr and abbr in abbr_to_name:
                            st_name = abbr_to_name[abbr]
                            col_idx = XNT_MAPPING[p_name]["col"]
                            
                            if st_name not in store_stock_data:
                                store_stock_data[st_name] = {i: 0 for i in range(0, 10)}
                            store_stock_data[st_name][col_idx] += closing
            
            tonkho_tbody = generate_tonkho_html(store_stock_data, name_to_abbr)

            # 4. Lấy dữ liệu Chuyến Xe (Trip)
            print("Đang tải dữ liệu Chuyến xe...")
            raw_trip_data = {}
            min_date = (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d')
            q_trip = f"""
            SELECT 
                DATE(t.t_departure),
                tl.tl_branch_id,
                tli.barrel_basket_code,
                tli.tli_transfer_qty,
                tli.tli_actual_received_qty
            FROM __cdc_kfm_kf_inventories_kf_trips_locations_items tli
            JOIN __cdc_kfm_kf_inventories_kf_trip_locations tl ON tli.tl_id = tl._id
            JOIN __cdc_kfm_kf_inventories_kf_trips t ON tl.t_id = t._id
            WHERE t.t_departure >= '{min_date}' AND tli.barrel_basket_code IS NOT NULL
            """
            cursor.execute(q_trip)
            for row in cursor.fetchall():
                d_val, b_id, basket_code, giao, thu = row
                if not d_val: continue
                date_str = d_val.strftime("%d/%m/%Y")
                abbr = branch_id_to_abbr.get(b_id)
                
                if abbr and abbr in abbr_to_name:
                    st_name = abbr_to_name[abbr]
                    giao = int(giao) if giao is not None else 0
                    thu = int(thu) if thu is not None else 0
                    
                    if date_str not in raw_trip_data:
                        raw_trip_data[date_str] = {}
                        
                    if abbr not in raw_trip_data[date_str]:
                        raw_trip_data[date_str][abbr] = {
                            "c": abbr,
                            "n": st_name,
                            "g": 0,
                            "t": 0,
                            "items": {}
                        }
                        
                    store_obj = raw_trip_data[date_str][abbr]
                    if basket_code not in store_obj["items"]:
                        store_obj["items"][basket_code] = [0, 0]
                    store_obj["items"][basket_code][0] += giao
                    store_obj["items"][basket_code][1] += thu
                    
                    if basket_code in COUNTABLE_TRIP_CODES:
                        store_obj["g"] += giao
                        store_obj["t"] += thu
                        
            # Chuyển raw_trip_data thành định dạng mảng (list)
            final_trip_data = {}
            for d, stores in raw_trip_data.items():
                final_trip_data[d] = list(stores.values())
                
            # Tạo key "all" (gộp tất cả các ngày)
            all_trips = []
            for d, st_list in final_trip_data.items():
                all_trips.extend(st_list)
                
            all_merged = {}
            import copy
            for st in all_trips:
                c = st["c"]
                if c not in all_merged:
                    all_merged[c] = copy.deepcopy(st)
                else:
                    all_merged[c]["g"] += st["g"]
                    all_merged[c]["t"] += st["t"]
                    for bk, counts in st["items"].items():
                        if bk not in all_merged[c]["items"]:
                            all_merged[c]["items"][bk] = [0, 0]
                        all_merged[c]["items"][bk][0] += counts[0]
                        all_merged[c]["items"][bk][1] += counts[1]
            
            final_trip_data["all"] = list(all_merged.values())
            trip_json_str = json.dumps(final_trip_data, ensure_ascii=False)
            
            # 5. Cập nhật index.html
            print("Đang cập nhật index.html...")
            new_html = re.sub(r'const TRIP_DATA\s*=\s*\{.*?\};', f'const TRIP_DATA = {trip_json_str};', html_content, flags=re.DOTALL)
            new_html = re.sub(
                r'<!-- TONKHO_TBODY_START -->.*?<!-- TONKHO_TBODY_END -->',
                f'<!-- TONKHO_TBODY_START -->\n<tbody>\n{tonkho_tbody}\n</tbody>\n<!-- TONKHO_TBODY_END -->',
                new_html,
                flags=re.DOTALL
            )
            
            # Generate Calendar Grid
            valid_dates = [d for d in final_trip_data.keys() if d != "all"]
            if valid_dates:
                valid_dates.sort(key=lambda x: datetime.strptime(x, "%d/%m/%Y"))
                min_date_iso = datetime.strptime(valid_dates[0], "%d/%m/%Y").strftime("%Y-%m-%d")
                max_date_iso = datetime.strptime(valid_dates[-1], "%d/%m/%Y").strftime("%Y-%m-%d")
                
                cal_html = ""
                for idx, d in enumerate(valid_dates):
                    d_obj = datetime.strptime(d, "%d/%m/%Y")
                    iso = d_obj.strftime("%Y-%m-%d")
                    day_str = d_obj.strftime("%d")
                    
                    chua_count = sum(1 for st in final_trip_data[d] if st["g"] > st["t"])
                    if chua_count == 0: continue
                    active_cls = " active" if idx == len(valid_dates) - 1 else ""
                    cal_html += f'<div class="cal-day{active_cls}" onclick="toggleDate(\'{d}\',this)" data-date="{d}" data-iso="{iso}"><div class="cal-date">{day_str}</div><div class="cal-badge"><span class="badge-nr">{chua_count}</span> chưa</div></div>\n'
                    
                new_html = re.sub(
                    r'<input type="date" id="date-from" value=".*?" min=".*?" max=".*?"',
                    f'<input type="date" id="date-from" value="{min_date_iso}" min="{min_date_iso}" max="{max_date_iso}"',
                    new_html
                )
                new_html = re.sub(
                    r'<input type="date" id="date-to" value=".*?" min=".*?" max=".*?"',
                    f'<input type="date" id="date-to" value="{max_date_iso}" min="{min_date_iso}" max="{max_date_iso}"',
                    new_html
                )
                new_html = re.sub(
                    r'<!-- CAL_GRID_START -->.*?<!-- CAL_GRID_END -->',
                    f'<!-- CAL_GRID_START -->\n{cal_html}<!-- CAL_GRID_END -->',
                    new_html,
                    flags=re.DOTALL
                )
                
            current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
            new_html = re.sub(r'(id="last-update-time"[^>]*>Cập nhật:\s*).*?(</div>)', r'\g<1>' + current_time + r'\2', new_html)
            
            backup_path = html_path + ".bak"
            shutil.copy2(html_path, backup_path)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_html)
                
            print(f"[OK] Cập nhật hoàn tất lúc {current_time}!")
            
    finally:
        conn.close()

if __name__ == "__main__":
    main()
