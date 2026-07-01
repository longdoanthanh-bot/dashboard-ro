import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Change missingBaskets calculation
old_missing = """              const diff = ig - it;
              if (diff > 0) {
                  missingBaskets[ic] = (missingBaskets[ic] || 0) + diff;
              }"""
new_missing = """              if (ig > 0 && it === 0) {
                  missingBaskets[ic] = (missingBaskets[ic] || 0) + ig;
              }"""
html = html.replace(old_missing, new_missing)

# Change top stats calculation
old_top_stats = """        stores.forEach(s => {
            const item = s.items[window.activeMissingFilter];
            if (item && item[0] > 0) {
                allG += item[0];
                allT += item[1];
                if (item[1] >= item[0]) allRc++; else allNr++;
            }
        });"""
new_top_stats = """        stores.forEach(s => {
            const item = s.items[window.activeMissingFilter];
            if (item && item[0] > 0 && item[1] === 0) {
                allG += item[0];
                allT += item[1];
                allNr++;
            }
        });"""
html = html.replace(old_top_stats, new_top_stats)

# Change renderStores filtering
old_render_stores = """        renderStores = renderStores.filter(s => {
            const item = s.items[window.activeMissingFilter];
            return item && (item[0] > item[1]);
        });"""
new_render_stores = """        renderStores = renderStores.filter(s => {
            const item = s.items[window.activeMissingFilter];
            return item && (item[0] > 0 && item[1] === 0);
        });"""
html = html.replace(old_render_stores, new_render_stores)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
