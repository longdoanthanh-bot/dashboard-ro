import os
for file in ['index.html', 'tasks.html', 'tele.html']:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f: content = f.read()
    if '<meta charset="UTF-8">' not in content:
        content = content.replace('<head>', '<head>\n  <meta charset="UTF-8">')
        with open(file, 'w', encoding='utf-8') as f: f.write(content)
