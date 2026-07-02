import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix TONKHO_TBODY
if '<!-- TONKHO_TBODY_START -->' not in html:
    html = html.replace('<tbody><tr class="tk-red"><td>1</td>', '<!-- TONKHO_TBODY_START -->\n<tbody><tr class="tk-red"><td>1</td>')
    html = html.replace('</tbody>\n        </table>\n    </div>\n</div>\n\n<!-- PANEL 2:', '</tbody>\n<!-- TONKHO_TBODY_END -->\n        </table>\n    </div>\n</div>\n\n<!-- PANEL 2:')
    print("Added TONKHO_TBODY markers")

# Fix CAL_GRID
if '<!-- CAL_GRID_START -->' not in html:
    html = html.replace('<div class="cal-grid">\n                <div class="cal-day "', '<div class="cal-grid">\n<!-- CAL_GRID_START -->\n                <div class="cal-day "')
    html = html.replace('<span class="badge-nr">12</span> chưa</div></div>\n\n            </div>', '<span class="badge-nr">12</span> chưa</div></div>\n<!-- CAL_GRID_END -->\n            </div>')
    print("Added CAL_GRID markers")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
