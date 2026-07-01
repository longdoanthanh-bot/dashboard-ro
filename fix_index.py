import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix navMenuContainer
content = re.sub(r'<div style="position: relative; display: flex; align-items: center; gap: 14px;"\s+id="navMenuContainer"\s+style="position: relative; display: flex; align-items: center; gap: 14px; flex-shrink: 0;">',
                 '<div style="position: relative; display: flex; align-items: center; gap: 14px; flex-shrink: 0;" id="navMenuContainer">',
                 content)

content = re.sub(r'<div style="position: relative; display: flex; align-items: center; gap: 14px; flex-shrink: 0;"\s+id="navMenuContainer"\s+style="position: relative; display: flex; align-items: center; gap: 14px; flex-shrink: 0;">',
                 '<div style="position: relative; display: flex; align-items: center; gap: 14px; flex-shrink: 0;" id="navMenuContainer">',
                 content)

# Remove duplicate TASKS HEADER CSS blocks
css_block = """/* ===== TASKS HEADER CSS ===== */
.add-form { display:flex; gap:8px; align-items:flex-end; background:transparent; padding:0; flex:1; max-width: 650px; justify-content: flex-end; }
.form-title { font-size:12px; font-weight:700; color:var(--text); margin-right:4px; margin-bottom: 6px; display:flex; align-items:center; }
.form-group { display:flex; flex-direction:column; gap:4px; }
.form-group label { font-size:9px; color:var(--text3); font-weight:600; text-transform:uppercase; letter-spacing:.5px; }
.form-input { padding:6px 10px; background:var(--bg2); border:1px solid var(--border); border-radius:6px; color:var(--text); font-size:11px; font-family:inherit; outline:none; transition:border-color .2s; }
.form-input:focus { border-color:var(--blue); }
.btn-create { padding:6px 16px; background:var(--blue); color:#fff; border:none; border-radius:6px; font-weight:600; font-size:11px; cursor:pointer; transition:background .2s; height: 28px; }
.btn-create:hover { background:#5a7aee; }
"""

# Count occurrences and keep only one
while content.count("/* ===== TASKS HEADER CSS ===== */") > 1:
    content = content.replace(css_block + "\n\n" + css_block, css_block)
    # If separated by other things, just do a regex replace
    content = re.sub(r'/\* ===== TASKS HEADER CSS ===== \*/.*?\.btn-create:hover \{ background:#5a7aee; \}', '', content, count=1, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Cleaned up index.html!")
