with open('index.html', 'rb') as f:
    c = f.read()
idx = c.find(b'<div class="map-stat-label">T')
print([hex(b) for b in c[idx+28:idx+38]])
