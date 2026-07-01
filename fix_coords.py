import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
json_path = r'G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master\store_coordinates.json'

with open(json_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

# Fix HTP
if 'HTP' in d:
    d['HTP']['lat'] = 10.7490
    d['HTP']['lng'] = 106.7328
    print("Fixed HTP coordinate.")

# Fix ECG (Eco Green)
if 'ECG' in d:
    # Eco Green is at Nguyen Van Linh / Tan Thuan Tay
    d['ECG']['lat'] = 10.7431
    d['ECG']['lng'] = 106.7153
    print("Fixed ECG coordinate.")

# Fix A220 & A165 (KDC Nam Long)
if 'A220' in d:
    d['A220']['lat'] = 10.7475
    d['A220']['lng'] = 106.7335
if 'A165' in d:
    d['A165']['lat'] = 10.7475
    d['A165']['lng'] = 106.7335
print("Fixed Nam Long coordinates.")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("Saved store_coordinates.json")
