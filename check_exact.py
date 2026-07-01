with open('index.html', 'rb') as f:
    c = f.read()

idx = c.find(b'<div class="map-stat-label">T')
print(c[idx:idx+150])
