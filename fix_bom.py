import os

def fix_bom(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    
    # Strip any number of BOMs at the beginning
    while content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
        
    # Write back with exactly one BOM
    with open(filename, 'wb') as f:
        f.write(b'\xef\xbb\xbf' + content)

fix_bom('index.html')
fix_bom('tasks.html')

print("BOMs fixed!")
