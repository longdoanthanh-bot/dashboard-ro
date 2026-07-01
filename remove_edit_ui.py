import re
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the "Sửa Tọa Độ" and "Tải JSON" buttons
html = re.sub(
    r'<button id="btnEditMap".*?</button>', 
    '', 
    html,
    flags=re.DOTALL
)
html = re.sub(
    r'<button id="btnDownloadMap".*?</button>', 
    '', 
    html,
    flags=re.DOTALL
)

# 2. Remove JavaScript related to Edit Mode
# We will just remove lines that contain 'window._isMapEditMode', 'btnEditMap', 'btnDownloadMap'
# or we can remove the entire block where we bind events.
html = re.sub(
    r'// Map Edit Mode.*?// End Map Edit Mode',
    '',
    html,
    flags=re.DOTALL
)

# 3. Also remove `draggable: window._isMapEditMode` logic
# We replace:
# const marker = L.marker([s.lat, s.lng], {icon: icon, draggable: window._isMapEditMode});
# with:
# const marker = L.marker([s.lat, s.lng], {icon: icon});
html = html.replace('{icon: icon, draggable: window._isMapEditMode}', '{icon: icon}')

# Remove dragend listener:
html = re.sub(
    r'marker\.on\("dragend".*?\}\);',
    '',
    html,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Removed map edit UI from index.html")
