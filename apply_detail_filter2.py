import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_detail = """        let detailItems = Object.entries(s.items)
            .filter(([ic,[g,t]]) => COUNTABLE_CODES.has(ic) && !(g===0 && t===0))
            .sort((a,b) => (b[1][0]-b[1][1]) - (a[1][0]-a[1][1]));
        for(const [ic, it] of detailItems) {"""

new_detail = """        let detailItems = Object.entries(s.items)
            .filter(([ic,[g,t]]) => COUNTABLE_CODES.has(ic) && !(g===0 && t===0));
        if (window.activeMissingFilter) {
            detailItems = detailItems.filter(([ic]) => ic === window.activeMissingFilter);
        }
        detailItems.sort((a,b) => (b[1][0]-b[1][1]) - (a[1][0]-a[1][1]));
        for(const [ic, it] of detailItems) {"""

if old_detail in html:
    html = html.replace(old_detail, new_detail)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Success")
else:
    print("Not found")
