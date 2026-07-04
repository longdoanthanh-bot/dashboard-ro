import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

if '<!-- TONKHO_TBODY_START -->' not in html:
    # Find the table and replace its tbody
    pattern = re.compile(r'(<table class="data-table" id="tonkho-table">.*?</thead>\s*)(<tbody>.*?</tbody>)', re.DOTALL)
    new_html = pattern.sub(r'\1\n<!-- TONKHO_TBODY_START -->\n\2\n<!-- TONKHO_TBODY_END -->', html)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Updated index.html")
else:
    print("Already updated")
