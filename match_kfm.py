import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('kfm_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

def find_stores(obj, depth=0):
    if depth > 10: return []
    res = []
    if isinstance(obj, dict):
        if 'lat' in obj and 'lng' in obj and 'address' in obj:
            res.append(obj)
        for k, v in obj.items():
            res.extend(find_stores(v, depth+1))
    elif isinstance(obj, list):
        for item in obj:
            res.extend(find_stores(item, depth+1))
    return res

stores = find_stores(d)
print(f"Found {len(stores)} store objects with lat, lng, address")
if stores:
    print(stores[0])

# Match our DB abbr/code with KFM website data
db = json.load(open(r'G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master\store_coordinates.json', encoding='utf-8'))

matched = 0
for k, v in db.items():
    if not v.get('address'): continue
    # Try to find a match in KFM stores by address similarity
    for ks in stores:
        # KFM address vs our address
        if ks['address'] and v['address']:
            # Normalize strings
            a1 = ks['address'].lower().replace(',', '').replace(' ', '')
            a2 = v['address'].lower().replace(',', '').replace(' ', '')
            if a1[:20] == a2[:20]: # if first 20 chars match
                v['lat'] = float(ks['lat'])
                v['lng'] = float(ks['lng'])
                matched += 1
                break

print(f"Matched {matched} out of {len(db)}")
if matched > 0:
    with open(r'G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master\store_coordinates.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print("Updated store_coordinates.json with precise coordinates from KFM website!")
