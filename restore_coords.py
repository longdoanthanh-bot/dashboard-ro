import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

json_path = r'G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master\store_coordinates.json'
with open(json_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

# Restore previous manual fixes for A197 and A144
if 'A197' in d:
    d['A197']['lat'] = 10.7686504
    d['A197']['lng'] = 106.7161671
if 'A144' in d:
    d['A144']['lat'] = 10.7431295
    d['A144']['lng'] = 106.6997426

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("Restored coordinates for A197 and A144")
