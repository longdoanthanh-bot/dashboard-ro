import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_logic = """    const stats = document.querySelectorAll('#panel-thuhoi .stat-num');
    if(stats[0]) stats[0].textContent = fmt(allNr);
    if(stats[1]) stats[1].textContent = fmt(allRc);
    if(stats[2]) stats[2].textContent = fmt(allG);
    if(stats[3]) stats[3].textContent = fmt(allT);
    
    if (window.activeMissingFilter && !missingBaskets[window.activeMissingFilter]) {
        window.activeMissingFilter = null;
    }
    let renderStores = stores;
    if (window.activeMissingFilter) {
        renderStores = renderStores.filter(s => {
            const item = s.items[window.activeMissingFilter];
            return item && (item[0] > 0 && item[1] === 0);
        });
    }"""

new_logic = """    if (window.activeMissingFilter && !missingBaskets[window.activeMissingFilter]) {
        window.activeMissingFilter = null;
    }
    
    if (window.activeMissingFilter) {
        allG = 0; allT = 0; allNr = 0; allRc = 0;
        stores.forEach(s => {
            const item = s.items[window.activeMissingFilter];
            if (item && item[0] > 0) {
                allG += item[0];
                allT += item[1];
                if (item[1] >= item[0]) allRc++; else allNr++;
            }
        });
    }

    const stats = document.querySelectorAll('#panel-thuhoi .stat-num');
    if(stats[0]) stats[0].textContent = fmt(allNr);
    if(stats[1]) stats[1].textContent = fmt(allRc);
    if(stats[2]) stats[2].textContent = fmt(allG);
    if(stats[3]) stats[3].textContent = fmt(allT);
    
    let renderStores = stores;
    if (window.activeMissingFilter) {
        renderStores = renderStores.filter(s => {
            const item = s.items[window.activeMissingFilter];
            return item && (item[0] > item[1]);
        });
    }"""

if old_logic in html:
    html = html.replace(old_logic, new_logic)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Success")
else:
    print("Not found")
