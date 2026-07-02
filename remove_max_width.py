import re

def remove_max_width(filepath, old_width):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # We want to change max-width:XXXXpx; to max-width:100%;
    # Wait, actually setting max-width:100% or just removing it is better.
    # We will replace max-width:1400px; with max-width:100%;
    
    html = html.replace(f'max-width:{old_width};', 'max-width:100%;')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated {filepath}")

remove_max_width('index.html', '1400px')
remove_max_width('tasks.html', '1500px')
