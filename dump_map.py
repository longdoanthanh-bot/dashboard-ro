import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

match = re.search(r'<!-- PANEL 3: SƠ ĐỒ ST -->(.*?)<div style="flex:1; display:flex; flex-direction:column;', html, re.DOTALL)
if match:
    print(match.group(1))
else:
    print("Not found")
