import json
import pandas as pd
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

_data_dir = os.environ.get('DATA_DIR', r"G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source")
json_path = os.path.join(_data_dir, 'Master', 'store_coordinates.json')
excel_path = os.path.join(_data_dir, 'Master', 'Danh sách ST.xlsx')

with open(json_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

df = pd.read_excel(excel_path)
cnt = 0

for _, r in df.iterrows():
    abbr = str(r.get('Tên viết tắt', ''))
    addr = str(r.get('Địa chỉ', ''))
    if not abbr or pd.isna(abbr): continue
    
    if abbr in d:
        old_addr = d[abbr].get('address', '')
        if old_addr != addr:
            print(f'{abbr}: "{old_addr}" -> "{addr}"')
            cnt += 1
            # Update dictionary
            d[abbr]['address'] = addr
            d[abbr]['lat'] = ""
            d[abbr]['lng'] = ""

print(f'Total diff: {cnt}')

if cnt > 0:
    # Save back
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("Updated store_coordinates.json")
