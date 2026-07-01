import os
import glob
import re
import json
import pandas as pd
from datetime import datetime

# Fix Windows console encoding
os.environ["PYTHONIOENCODING"] = "utf-8"
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(PROJECT_DIR, "index.html")

# Paths
xnt_dir = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Tồn kho Rổ"
trip_dir = r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Trip"

def find_latest_excel(directory, prefix):
    pattern = os.path.join(directory, f"{prefix}*.xlsx")
    files = glob.glob(pattern)
    if not files:
        return None
    # Sort by modification time
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

# Mapping Tên hàng to Column Index and Warehouse in index.html
XNT_MAPPING = {
    "Rổ nhựa đen/xanh lá kho rau": {"col": 1, "wh": "Rau"},
    "Seedlog - Thùng tote xanh lá, xanh dương không đục lỗ": {"col": 2, "wh": "Khô"},
    "Rổ đen xếp chồng quai đỏ": {"col": 3, "wh": "Rau"},
    "Rổ nhựa đỏ kích thước 60x40x24 cm": {"col": 4, "wh": "Dòng Mát"},
    "Rổ cam xếp chồng quai đỏ (sóng nhựa hở BPGST-25V KT: 600x400x250)": {"col": 5, "wh": ""},
    "Rổ ABA đông mát": {"col": 6, "wh": "Dòng Mát"},
    "Tote ABA đông mát": {"col": 7, "wh": "Dòng Mát"},
    "Tote đỏ bánh tươi": {"col": 8, "wh": "Rau"}
}

COUNTABLE_TRIP_CODES = {"B0001", "B0016", "B0015", "B0012", "B0017"}

def parse_xnt_file(file_path):
    print(f"Reading XNT: {file_path}")
    df = pd.read_excel(file_path)
    
    # We want: Chi nhánh -> {col_index: Tồn cuối kỳ}
    store_data = {}
    
    for _, row in df.iterrows():
        chi_nhanh = str(row.get('Chi nhánh', ''))
        if not chi_nhanh or pd.isna(chi_nhanh):
            continue
            
        # extract abbr and name. E.g. "KFM_HCM_Q7 - Cửa Hàng Siêu Thị Sỉ"
        st_name = chi_nhanh
            
        ten_hang = str(row.get('Tên hàng', ''))
        ton_cuoi_ky = row.get('Tồn cuối kỳ', 0)
        
        # skip NaN ton_cuoi_ky
        if pd.isna(ton_cuoi_ky):
            ton_cuoi_ky = 0
        else:
            ton_cuoi_ky = int(ton_cuoi_ky)
            
        if ten_hang in XNT_MAPPING:
            col_idx = XNT_MAPPING[ten_hang]["col"]
            
            if st_name not in store_data:
                store_data[st_name] = {i: 0 for i in range(1, 9)}
            
            store_data[st_name][col_idx] += ton_cuoi_ky
            
    return store_data

def generate_tonkho_html(store_data, store_coords):
    # Mapping name to abbr based on STORE_COORDS
    name_to_abbr = {s["name"]: s["abbr"] for s in store_coords if "name" in s and "abbr" in s}
    
    html_rows = []
    idx = 1
    
    # sort store_data by total Ton Kho (descending)
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
        
        for col_idx in range(1, 9):
            val = cols.get(col_idx, 0)
            
            # Find warehouse for this col
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

def parse_trip_file(file_path):
    print(f"Reading TRIP: {file_path}")
    df = pd.read_excel(file_path)
    
    # We want: { date: [ { c: abbr, n: name, g: total_giao, t: total_thu, items: { basket_code: [giao, thu] } } ] }
    trip_data = {}
    
    for _, row in df.iterrows():
        date = str(row.get('Ngày xuất phát', ''))
        if pd.isna(date) or not date:
            continue
            
        # Optional: format date "2026-06-26 00:00:00" to "26/06/2026"
        if " " in date:
            date = date.split(" ")[0]
        if "-" in date:
            # Assuming YYYY-MM-DD
            parts = date.split("-")
            if len(parts) == 3:
                date = f"{parts[2]}/{parts[1]}/{parts[0]}"
                
        abbr = str(row.get('Nơi nhận (Tên viết tắt)', ''))
        name = str(row.get('Nơi nhận (Tên)', ''))
        basket_code = str(row.get('Mã thùng, rổ', ''))
        giao = row.get('Số lượng giao', 0)
        thu = row.get('Số lượng thu hồi', 0)
        
        if pd.isna(giao): giao = 0
        if pd.isna(thu): thu = 0
        giao = int(giao)
        thu = int(thu)
        
        if pd.isna(abbr) or not abbr:
            continue
            
        if date not in trip_data:
            trip_data[date] = {}
            
        store_key = abbr
        if store_key not in trip_data[date]:
            trip_data[date][store_key] = {
                "c": abbr,
                "n": name,
                "g": 0,
                "t": 0,
                "items": {}
            }
            
        store_obj = trip_data[date][store_key]
        if basket_code not in store_obj["items"]:
            store_obj["items"][basket_code] = [0, 0]
            
        store_obj["items"][basket_code][0] += giao
        store_obj["items"][basket_code][1] += thu
        
        # update totals
        if basket_code in COUNTABLE_TRIP_CODES:
            store_obj["g"] += giao
            store_obj["t"] += thu
            
    # Convert inner dict to list
    final_trip_data = {}
    for d, stores in trip_data.items():
        final_trip_data[d] = list(stores.values())
        
    return final_trip_data

def main():
    xnt_file = find_latest_excel(xnt_dir, "XNT_")
    trip_file = find_latest_excel(trip_dir, "DS-chi-tiet-chuyen-xe_")
    
    if not xnt_file or not trip_file:
        print("Could not find required Excel files.")
        sys.exit(1)
        
    # Read STORE_COORDS from index.html to map names
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    match = re.search(r'const STORE_COORDS\s*=\s*(\[.*?\]);', html_content, re.DOTALL)
    if not match:
        print("Could not find STORE_COORDS in index.html")
        sys.exit(1)
        
    store_coords = json.loads(match.group(1))
    
    # 1. Parse XNT
    xnt_data = parse_xnt_file(xnt_file)
    tonkho_tbody = generate_tonkho_html(xnt_data, store_coords)
    
    # 2. Parse TRIP
    trip_data = parse_trip_file(trip_file)
    # create a combined "all" key for trip data just in case
    all_trips = []
    for d, st_list in trip_data.items():
        all_trips.extend(st_list)
    
    # Merge same stores in "all"
    all_merged = {}
    for st in all_trips:
        c = st["c"]
        if c not in all_merged:
            import copy
            all_merged[c] = copy.deepcopy(st)
        else:
            all_merged[c]["g"] += st["g"]
            all_merged[c]["t"] += st["t"]
            for bk, counts in st["items"].items():
                if bk not in all_merged[c]["items"]:
                    all_merged[c]["items"][bk] = [0, 0]
                all_merged[c]["items"][bk][0] += counts[0]
                all_merged[c]["items"][bk][1] += counts[1]
                
    trip_data["all"] = list(all_merged.values())
    trip_json_str = json.dumps(trip_data, ensure_ascii=False)
    
    # 3. Update index.html
    # Update TRIP_DATA
    new_html = re.sub(r'const TRIP_DATA\s*=\s*\{.*?\};', f'const TRIP_DATA = {trip_json_str};', html_content, flags=re.DOTALL)
    
    # Update TONKHO_TBODY
    new_html = re.sub(
        r'<!-- TONKHO_TBODY_START -->.*?<!-- TONKHO_TBODY_END -->',
        f'<!-- TONKHO_TBODY_START -->\n<tbody>\n{tonkho_tbody}\n</tbody>\n<!-- TONKHO_TBODY_END -->',
        new_html,
        flags=re.DOTALL
    )
    
    # Generate Calendar Grid and update Date Pickers
    valid_dates = [d for d in trip_data.keys() if d != "all"]
    if valid_dates:
        valid_dates.sort(key=lambda x: datetime.strptime(x, "%d/%m/%Y"))
        min_date_iso = datetime.strptime(valid_dates[0], "%d/%m/%Y").strftime("%Y-%m-%d")
        max_date_iso = datetime.strptime(valid_dates[-1], "%d/%m/%Y").strftime("%Y-%m-%d")
        
        cal_html = ""
        for idx, d in enumerate(valid_dates):
            d_obj = datetime.strptime(d, "%d/%m/%Y")
            iso = d_obj.strftime("%Y-%m-%d")
            day_str = d_obj.strftime("%d")
            
            # count "chua"
            chua_count = sum(1 for st in trip_data[d] if st["g"] > st["t"])
            
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
    
    # Update timestamp
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    new_html = re.sub(r'<div>Cập nhật:.*?</div>', f'<div>Cập nhật: {current_time}</div>', new_html)
    
    # Write back
    backup_path = html_path + ".bak"
    import shutil
    shutil.copy2(html_path, backup_path)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print(f"Successfully updated index.html with XNT ({os.path.basename(xnt_file)}) and TRIP ({os.path.basename(trip_file)}) at {current_time}")

if __name__ == "__main__":
    main()
