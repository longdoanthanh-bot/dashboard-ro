import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8-sig') as f:
    content = f.read()

changes = 0

# Reduce header padding
old = '.header { position:relative; z-index:9999; padding:24px 36px;'
new = '.header { position:relative; z-index:9999; padding:12px 24px;'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('OK: header padding reduced')

# Reduce avatar
if 'width="60" height="60"' in content:
    content = content.replace('width="60" height="60"', 'width="44" height="44"', 1)
    changes += 1
    print('OK: avatar size reduced')

# Reduce container top padding
if 'padding:20px 36px' in content:
    content = content.replace('padding:20px 36px', 'padding:8px 24px')
    changes += 1
    print('OK: container padding reduced')

if changes > 0:
    with open('index.html', 'w', encoding='utf-8-sig') as f:
        f.write(content)

print(f'DONE: {changes} changes')
