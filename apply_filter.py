import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add window.activeMissingFilter and toggleMissingFilter function
script_to_add = """
window.activeMissingFilter = null;
function toggleMissingFilter(ic) {
    if (window.activeMissingFilter === ic) {
        window.activeMissingFilter = null;
    } else {
        window.activeMissingFilter = ic;
    }
    renderTripTable();
}
"""
if "window.activeMissingFilter" not in html:
    html = html.replace("function renderTripTable() {", script_to_add + "\nfunction renderTripTable() {")

# 2. Modify the mapping in bSumContent
old_map = """              bSumContent.innerHTML = mKeys.map(ic => {
                  const bName = BASKET_NAMES[ic] || ic;
                  return `<div style="background:rgba(248,113,113,0.1); border:1px solid rgba(248,113,113,0.3); color:var(--red); padding:4px 10px; border-radius:6px; font-size:11px; font-weight:600; display:flex; align-items:center; gap:6px;">
                      ${bName}: <span style="font-size:13px; font-weight:800;">${fmt(missingBaskets[ic])}</span>
                  </div>`;
              }).join('');"""

new_map = """              bSumContent.innerHTML = mKeys.map(ic => {
                  const bName = BASKET_NAMES[ic] || ic;
                  const isActive = (window.activeMissingFilter === ic);
                  const bg = isActive ? 'var(--red)' : 'rgba(248,113,113,0.1)';
                  const color = isActive ? '#fff' : 'var(--red)';
                  return `<div onclick="toggleMissingFilter('${ic}')" title="Click để lọc các ST có thu hồi loại rổ này = 0" style="cursor:pointer; background:${bg}; border:1px solid rgba(248,113,113,0.3); color:${color}; padding:4px 10px; border-radius:6px; font-size:11px; font-weight:600; display:flex; align-items:center; gap:6px; transition:all 0.2s;">
                      ${bName}: <span style="font-size:13px; font-weight:800;">${fmt(missingBaskets[ic])}</span>
                  </div>`;
              }).join('');"""
html = html.replace(old_map, new_map)

# 3. Add filtering of `stores` before `slice(0, tripTopN)`
old_display = """      const displayStores = stores.slice(0, tripTopN);
      const tbody = document.getElementById('trip-tbody');"""

new_display = """      if (window.activeMissingFilter && !missingBaskets[window.activeMissingFilter]) {
          window.activeMissingFilter = null; // reset if filter is no longer in missing baskets
      }
      let renderStores = stores;
      if (window.activeMissingFilter) {
          renderStores = renderStores.filter(s => {
              const item = s.items[window.activeMissingFilter];
              return item && (item[0] > 0 && item[1] === 0);
          });
      }
      const displayStores = renderStores.slice(0, tripTopN);
      const tbody = document.getElementById('trip-tbody');"""
html = html.replace(old_display, new_display)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
