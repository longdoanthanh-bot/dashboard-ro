import json
import pandas as pd
import sys
import time
import urllib.request
import urllib.parse
import re

sys.stdout.reconfigure(encoding='utf-8')

json_path = r'G:\My Drive\ANTIGRAVITY\GIAO_VAN\Rổ\Data_Source\Master\store_coordinates.json'

with open(json_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

def clean_address(addr):
    parts = [p.strip() for p in addr.split(',')]
    bad_prefixes = ["chung cư", "block", "shophouse", "tầng", "tháp", "căn", "lô", "kcn", "khu", "kho", "ô ", "số "]
    
    good_parts = []
    for p in parts:
        p_lower = p.lower()
        is_bad = False
        for bp in bad_prefixes:
            if p_lower.startswith(bp):
                is_bad = True
                break
        if not is_bad:
            good_parts.append(p)
            
    if len(good_parts) > 0:
        return ", ".join(good_parts)
    return addr

def extract_street_and_city(addr):
    # Try to just get the street and the city to broaden the search
    parts = [p.strip() for p in addr.split(',')]
    if len(parts) >= 3:
        # take the part with the street number or name, and the last part (city)
        return parts[-3] + ", " + parts[-1]
    return addr

def geocode_query(query):
    query_enc = urllib.parse.quote(query)
    url = f"https://nominatim.openstreetmap.org/search?q={query_enc}&format=json&limit=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'KingFoodMart-Dashboard-Auto-Updater/1.1'})
    try:
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode('utf-8'))
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Error querying {query}: {e}")
    return None, None

cnt = 0
for k, v in d.items():
    if 'address' not in v or not v['address']:
        continue
    if 'lat' in v and 'lng' in v:
        # Check if coordinates are 0 or empty
        if v['lat'] and v['lng']:
            continue

    # Try to geocode
    addr = v['address']
    print(f"Geocoding missing coords for {k}...")
    
    # Strategy 1: Raw
    lat, lng = geocode_query(addr)
    time.sleep(1.5)
    
    # Strategy 2: Cleaned
    if not lat:
        clean = clean_address(addr)
        if clean != addr:
            print(f"  Fallback 1: {clean}")
            lat, lng = geocode_query(clean)
            time.sleep(1.5)
            
    # Strategy 3: Broaden
    if not lat:
        broad = extract_street_and_city(addr)
        if broad != addr and broad != clean_address(addr):
            print(f"  Fallback 2: {broad}")
            lat, lng = geocode_query(broad)
            time.sleep(1.5)
            
    if lat:
        v['lat'] = lat
        v['lng'] = lng
        print(f"✅ Success {k} -> {lat}, {lng}")
        cnt += 1
    else:
        print(f"❌ Failed to find: {k} - {addr}")

if cnt > 0:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"Updated {cnt} missing coordinates in store_coordinates.json")
else:
    print("No new coordinates found.")
