import re

with open('tasks.html', 'r', encoding='utf-8') as f:
    tc = f.read()
    
# Extract all add-form related CSS
# From /* ===== ADD TASK FORM ===== */ to .checklist-item-delete:hover
start = tc.find('/* ===== ADD TASK FORM ===== */')
end = tc.find('.checklist-item-delete:hover', start)
form_css = tc[start:end].strip()

# Update .add-form to be horizontal
# Replace flex-wrap:wrap with flex-wrap:nowrap; overflow-x:auto
form_css = form_css.replace('flex-wrap:wrap;', 'flex-wrap:nowrap; overflow-x:auto; background:transparent; border:none; padding:0;')
# Replace gap:10px with gap:12px
form_css = form_css.replace('gap:10px;', 'gap:12px;')

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

# Inject into index.html
style_end = idx.find('</style>')
idx = idx[:style_end] + form_css + '\n' + idx[style_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

print("Injected CSS!")
