import os
import re
import json
import glob
import shutil
import pymysql
import pandas as pd
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
    "TOTE RỔ ĐEN CÓ NẮP": {"col": 9, "wh": "Thịt Cá SCF"},
    "Tote xanh dương đựng cá": {"col": 10, "wh": "Thịt Cá SCF"}
}

DB_TRIP_TO_COL = {
    "B0015": 1, # Rổ đen xếp chồng quai đỏ
    "CC00392": 2, # Rổ ABA đông mát
    "B0017": 4, # Tote đỏ bánh tươi
    "B0012": 5, # Rổ nhựa đỏ kích thước 60x40x24 cm
    "B0016": 7, # ITL Thùng tote xanh dương đục lỗ
    "B0001": 8, # Seedlog Thùng tote xanh lá, xanh dương không đục lỗ
    "CC00391": 10, # Tote xanh dương đựng cá
}

COUNTABLE_TRIP_CODES = {"B0001", "B0016", "B0015", "B0012", "B0017", "CC00392", "CC00391"}

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
        
        for col_idx in range(0, 11):
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
    valid_coords = []
    for s in store_coords:
        if "name" not in s or "abbr" not in s: continue
        name_lower = s["name"].lower()
        store_type = s.get("store_type", "").lower()
        if "kho" in name_lower or "kho" in store_type:
            continue
        valid_coords.append(s)
        
    abbr_to_name = {s["abbr"]: s["name"] for s in valid_coords}
    name_to_abbr = {s["name"]: s["abbr"] for s in valid_coords}

    conn = pymysql.connect(**DB_CONFIG)
    
    try:
        with conn.cursor() as cursor:
            # 2. Xây dựng Mapping
            print("Đang tải mapping Cửa hàng & Sản phẩm...")
            cursor.execute("SELECT DISTINCT branch_id, branch_code, branch_name FROM __cdc_kfm_kf_inventories_kf_inventory_transaction_stockcard WHERE branch_code IS NOT NULL AND branch_code != ''")
            branch_id_to_code = {}
            branch_id_to_name = {}
            for row in cursor.fetchall():
                branch_id_to_code[row[0]] = row[1]
                if row[2]:
                    branch_id_to_name[row[0]] = row[2]
            
            cursor.execute("SELECT DISTINCT barcode, product_name FROM __cdc_kfm_kf_inventories_kf_inventory_transaction_stockcard WHERE product_name IS NOT NULL")
            barcode_to_product_name = {row[0]: row[1] for row in cursor.fetchall()}

            # 3. Lấy dữ liệu Tồn Kho từ EXCEL (DB không có 'Tồn cuối kỳ' chính xác)
            print("Đang tải dữ liệu Tồn kho từ Excel...")
            store_stock_data = {}
            
            _data_dir = os.environ.get('DATA_DIR', '')
            _local_xnt = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'TonKhoRo')
            _gdrive_xnt = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Tồn kho Rổ"
            if _data_dir:
                xnt_dir = os.path.join(_data_dir, "TonKhoRo")
            elif os.path.isdir(_local_xnt) and glob.glob(os.path.join(_local_xnt, "XNT_*.xlsx")):
                xnt_dir = _local_xnt
            else:
                xnt_dir = _gdrive_xnt
            xnt_files = glob.glob(os.path.join(xnt_dir, "XNT_*.xlsx"))

            def parse_date(f):
                m = re.search(r'(\d{2})(\d{2})(\d{4})', os.path.basename(f))
                try:
                    return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
                except:
                    return datetime.min
        
            xnt_files.sort(key=parse_date, reverse=True)
            latest_xnt_file = xnt_files[0] if xnt_files else None
            excel_date = parse_date(latest_xnt_file).date() if latest_xnt_file else datetime.min.date()

            if latest_xnt_file:
                print(f"  File XNT: {os.path.basename(latest_xnt_file)}")
                df_xnt = pd.read_excel(latest_xnt_file)
                for _, row in df_xnt.iterrows():
                    ten_hang = str(row.get('Tên hàng', '')).strip()
                    if ten_hang not in XNT_MAPPING:
                        continue
                    ton_cuoi = row.get('Tồn cuối kỳ', 0)
                    if pd.isna(ton_cuoi) or int(ton_cuoi) == 0:
                        continue
                    ton_cuoi = int(ton_cuoi)
                    chi_nhanh = str(row.get('Chi nhánh', '')).strip()
                    
                    # Map chi_nhanh → STORE_COORDS name
                    st_name = None
                    if chi_nhanh in name_to_abbr:
                        st_name = chi_nhanh
                    else:
                        # Thử match một phần
                        for sc_name in name_to_abbr:
                            if chi_nhanh in sc_name or sc_name in chi_nhanh:
                                st_name = sc_name
                                break
                    if not st_name:
                        continue
                    
                    col_idx = XNT_MAPPING[ten_hang]["col"]
                    if st_name not in store_stock_data:
                        store_stock_data[st_name] = {i: 0 for i in range(0, 11)}
                    store_stock_data[st_name][col_idx] += ton_cuoi
            else:
                print("  ⚠️ Không tìm thấy file XNT!")

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
                
                # Map qua branch_name hoặc fallback qua branch_code
                st_name = branch_id_to_name.get(b_id)
                if st_name and st_name in name_to_abbr:
                    abbr = name_to_abbr[st_name]
                else:
                    abbr = branch_id_to_code.get(b_id)
                    if abbr and abbr in abbr_to_name:
                        st_name = abbr_to_name[abbr]
                    else:
                        continue
                
                giao = int(giao) if giao is not None else 0
                thu = int(thu) if thu is not None else 0
                
                # Trip data aggregation for UI (not for inventory modification)
                    
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
            
            tonkho_tbody = generate_tonkho_html(store_stock_data, name_to_abbr)
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
            
            valid_dates_all = [d for d in final_trip_data.keys() if d != "all"]
            
            # Format metadata
            if valid_dates_all:
                latest_trip = max(valid_dates_all, key=lambda x: datetime.strptime(x, "%d/%m/%Y"))
            else:
                latest_trip = "N/A"
            meta_str = f"Tồn kho: {os.path.basename(latest_xnt_file) if latest_xnt_file else 'N/A'} | Trip: DB (Tới {latest_trip})"
            new_html = re.sub(
                r'<!-- METADATA_START -->.*?<!-- METADATA_END -->',
                f'<!-- METADATA_START -->{meta_str}<!-- METADATA_END -->',
                new_html,
                flags=re.DOTALL
            )
            
            # Generate Calendar Grid - chỉ hiển thị 5 ngày gần nhất từ today lùi lại
            valid_dates = valid_dates_all[:]
            if valid_dates:
                valid_dates.sort(key=lambda x: datetime.strptime(x, "%d/%m/%Y"))
                # Chỉ lấy 5 ngày gần nhất
                today = datetime.now().date()
                valid_dates = [d for d in valid_dates if datetime.strptime(d, "%d/%m/%Y").date() <= today]
                valid_dates = valid_dates[-5:]  # Lấy 5 ngày cuối (gần nhất)
                
                min_date_iso = datetime.strptime(valid_dates[0], "%d/%m/%Y").strftime("%Y-%m-%d")
                max_date_iso = datetime.strptime(valid_dates[-1], "%d/%m/%Y").strftime("%Y-%m-%d")
                
                cal_html = ""
                for idx, d in enumerate(valid_dates):
                    d_obj = datetime.strptime(d, "%d/%m/%Y")
                    iso = d_obj.strftime("%Y-%m-%d")
                    day_str = d_obj.strftime("%d")
                    
                    chua_count = sum(1 for st in final_trip_data[d] if st["g"] > st["t"])
                    if chua_count == 0: continue
                    active_cls = " active"  # Tất cả ngày đều active mặc định
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
            
            # === AUTO CHANGELOG ===
            total_giao_cl = sum(st['g'] for d, sts in final_trip_data.items() if d != 'all' for st in sts)
            total_thu_cl = sum(st['t'] for d, sts in final_trip_data.items() if d != 'all' for st in sts)
            num_days_cl = len([d for d in final_trip_data.keys() if d != 'all'])
            num_stores_cl = len(store_stock_data)
            today_str = datetime.now().strftime("%d/%m/%Y")
            pct_thu = round(total_thu_cl / total_giao_cl * 100, 1) if total_giao_cl > 0 else 0
            chua_count_cl = sum(1 for d, sts in final_trip_data.items() if d != 'all' for st in sts if st['g'] > st['t'])
            
            cl_entry = (
                f'<div class="cl-entry">'
                f'<div class="cl-dot improve"></div>'
                f'<div class="cl-card">'
                f'<div class="cl-date">{current_time}</div>'
                f'<div class="cl-title">📊 Cập nhật dữ liệu tự động</div>'
                f'<div class="cl-body">'
                f'📁 <strong>{os.path.basename(latest_xnt_file) if latest_xnt_file else "(không tìm thấy)"}</strong> + DB trip<br>'
                f'🏪 <strong>{num_stores_cl}</strong> ST tồn kho · '
                f'📅 <strong>{num_days_cl}</strong> ngày trip · '
                f'Giao: <strong>{total_giao_cl:,}</strong> · '
                f'Thu: <strong>{total_thu_cl:,}</strong> ({pct_thu}%) · '
                f'Chưa thu: <strong>{chua_count_cl}</strong> lượt'
                f'</div></div></div>\n'
            )
            
            auto_match = re.search(
                r'<!-- CHANGELOG_AUTO_START -->(.*?)<!-- CHANGELOG_AUTO_END -->',
                new_html, flags=re.DOTALL
            )
            if auto_match:
                existing_auto = auto_match.group(1)
                entries = re.findall(r'<div class="cl-entry">.*?</div>\s*</div>\s*</div>', existing_auto, flags=re.DOTALL)
                today_exists = False
                new_entries = []
                for entry in entries:
                    date_m = re.search(r'<div class="cl-date">(\d{2}/\d{2}/\d{4})', entry)
                    if date_m and date_m.group(1) == today_str:
                        today_exists = True
                        new_entries.append(cl_entry)
                    else:
                        new_entries.append(entry + '\n')
                if not today_exists:
                    new_entries.insert(0, cl_entry)
                new_entries = new_entries[:7]
                auto_block = '\n'.join(new_entries)
                new_html = re.sub(
                    r'<!-- CHANGELOG_AUTO_START -->.*?<!-- CHANGELOG_AUTO_END -->',
                    f'<!-- CHANGELOG_AUTO_START -->\n{auto_block}<!-- CHANGELOG_AUTO_END -->',
                    new_html, flags=re.DOTALL
                )
            
            # Summary
            summary = {
                "time": current_time,
                "source": "DB",
                "stores": num_stores_cl,
                "days": num_days_cl,
                "total_giao": total_giao_cl,
                "total_thu": total_thu_cl
            }
            import json as _json
            summary_js = _json.dumps(summary, ensure_ascii=False)
            marker = '// %%LAST_UPDATE_SUMMARY%%'
            if marker in new_html:
                new_html = re.sub(
                    r'// %%LAST_UPDATE_SUMMARY%%.*?// %%END_SUMMARY%%',
                    f'{marker}\nwindow.LAST_UPDATE = {summary_js};\n// %%END_SUMMARY%%',
                    new_html, flags=re.DOTALL
                )
            
            summary_path = os.path.join(os.path.dirname(html_path), 'data', 'last_update.json')
            with open(summary_path, 'w', encoding='utf-8') as f:
                _json.dump(summary, f, ensure_ascii=False, indent=2)
            
            backup_path = html_path + ".bak"
            shutil.copy2(html_path, backup_path)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_html)
                
            print(f"\n{'='*50}")
            print(f"📊 KẾT QUẢ CẬP NHẬT ({current_time})")
            print("==================================================")
            print(f"📁 Tồn kho: {os.path.basename(latest_xnt_file) if latest_xnt_file else '(không tìm thấy)'} | Trip: DB trực tiếp")
            print(f"🏪 Số cửa hàng tồn kho: {num_stores_cl}")
            print(f"📅 Số ngày trip: {num_days_cl}")
            print(f"📦 Tổng giao: {total_giao_cl:,} | Tổng thu: {total_thu_cl:,} ({pct_thu}%)")
            print(f"{'='*50}")
            
    finally:
        conn.close()

if __name__ == "__main__":
    main()
