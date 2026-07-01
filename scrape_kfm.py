import urllib.request
import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://kingfoodmart.com/he-thong-sieu-thi', headers={'User-Agent': 'Mozilla/5.0'})
try:
    res = urllib.request.urlopen(req)
    html = res.read().decode('utf-8')
    # Try to find a JSON payload in Next.js __NEXT_DATA__
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
    if match:
        data = json.loads(match.group(1))
        # Navigate the JSON structure to find stores. Usually in props.pageProps
        print("Found __NEXT_DATA__")
        with open('kfm_data.json', 'w', encoding='utf-8') as f:
            f.write(match.group(1))
    else:
        print("No __NEXT_DATA__ found")
except Exception as e:
    print(e)
