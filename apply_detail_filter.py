import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Modify `displayStores.forEach`
old_loop_start = """      let tG=0, tT=0;
      displayStores.forEach((s,i) => {
          const g=s.fg, t=s.ft, diff=g-t;
          tG+=g; tT+=t;
          let rowCls,statusCls,statusLabel;"""

new_loop_start = """      let tG=0, tT=0;
      displayStores.forEach((s,i) => {
          let g=s.fg, t=s.ft;
          if (window.activeMissingFilter) {
              const item = s.items[window.activeMissingFilter];
              if (item) { g = item[0]; t = item[1]; }
          }
          const diff=g-t;
          tG+=g; tT+=t;
          let rowCls,statusCls,statusLabel;"""

html = html.replace(old_loop_start, new_loop_start)


old_detail = """          let detailItems = Object.entries(s.items)
              .filter(([ic,[g,t]]) => COUNTABLE_CODES.has(ic) && !(g===0 && t===0))
              .sort((a,b) => (b[1][0]-b[1][1]) - (a[1][0]-a[1][1]));
          for(const [ic, it] of detailItems) {"""

new_detail = """          let detailItems = Object.entries(s.items)
              .filter(([ic,[g,t]]) => COUNTABLE_CODES.has(ic) && !(g===0 && t===0));
          if (window.activeMissingFilter) {
              detailItems = detailItems.filter(([ic]) => ic === window.activeMissingFilter);
          }
          detailItems.sort((a,b) => (b[1][0]-b[1][1]) - (a[1][0]-a[1][1]));
          for(const [ic, it] of detailItems) {"""

html = html.replace(old_detail, new_detail)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
