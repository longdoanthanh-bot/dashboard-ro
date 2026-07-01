import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Remove HTML for basket-summary-panel
c = re.sub(r'<div class="basket-summary-panel" id="basket-summary".*?</div>\s*</div>', '', c, flags=re.DOTALL)

# Remove JS
js_pattern = r"const bSumPanel = document\.getElementById\('basket-summary'\);.*?if \(window\.activeMissingFilter && !missingBaskets\[window\.activeMissingFilter\]\) \{\s*window\.activeMissingFilter = null;\s*\}"
c = re.sub(js_pattern, '', c, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8-sig') as f:
    f.write(c)

print("Basket summary completely removed.")
