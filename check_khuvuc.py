import json
import pandas as pd
import sys
import glob
import os

sys.stdout.reconfigure(encoding='utf-8')

json_path = r'G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master\store_coordinates.json'

def find_latest_excel(directory, prefix):
    pattern = os.path.join(directory, f"{prefix}*.xlsx")
    files = glob.glob(pattern)
    if not files: return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

excel_path = find_latest_excel(r'G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master', 'DS-khu-vuc')
if not excel_path:
    print("No DS-khu-vuc file found")
    sys.exit(0)

print(f"Checking against {os.path.basename(excel_path)}")

with open(json_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

df = pd.read_excel(excel_path)
cnt = 0

for _, r in df.iterrows():
    abbr = str(r.get('Tên viết tắt', '')).strip()
    addr = str(r.get('Địa chỉ', '')).strip()
    if not abbr or pd.isna(abbr) or abbr == 'nan': continue
    
    if abbr in d:
        old_addr = d[abbr].get('address', '').strip()
        if old_addr != addr and addr and addr != 'nan':
            print(f'{abbr}: "{old_addr}" -> "{addr}"')
            cnt += 1
            # Update dictionary and CLEAR lat/lng so geocode.py can pick it up
            d[abbr]['address'] = addr
            d[abbr]['lat'] = 0.0
            d[abbr]['lng'] = 0.0

print(f'Total diff: {cnt}')

if cnt > 0:
    # Save back
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("Updated store_coordinates.json. Now you should run geocode.py")
