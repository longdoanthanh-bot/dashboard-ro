import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the ReferenceError: diff is not defined
html = html.replace(
    'if (ig > 0 && it === 0) {\n                missingBaskets[ic] = (missingBaskets[ic] || 0) + diff;\n            }',
    'if (ig > 0 && it === 0) {\n                missingBaskets[ic] = (missingBaskets[ic] || 0) + ig;\n            }'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
