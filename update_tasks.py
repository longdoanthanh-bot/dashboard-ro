import re

with open('tasks.html', 'r', encoding='utf-8') as f:
    html = f.read()

changed = False

# 1. Swap order
start_form = html.find('<!-- ADD TASK FORM -->')
start_stats = html.find('<!-- STATS — RIGHT SIDE -->')
end_stats = html.find('<!-- FILTER TABS -->')

if start_form != -1 and start_stats != -1 and end_stats != -1 and start_form < start_stats:
    form_html = html[start_form:start_stats].strip()
    top_row_end = html.rfind('</div>', start_stats, end_stats)
    
    if top_row_end != -1:
        stats_html = html[start_stats:top_row_end].strip()
        top_row_start = html.find('<div class="top-row">') + len('<div class="top-row">')
        
        # Change comment text just to be correct
        stats_html = stats_html.replace('STATS — RIGHT SIDE', 'STATS — LEFT SIDE')
        form_html = form_html.replace('ADD TASK FORM', 'ADD TASK FORM — RIGHT SIDE')
        
        new_top_row_content = f'\n        {stats_html}\n\n        {form_html}\n    '
        html = html[:top_row_start] + new_top_row_content + html[top_row_end:]
        print("Swapped sections")
        changed = True

# 2. Change CSS for stat-right-group
css_pattern = r'(\.stat-right-group\s*\{[^}]*?flex-direction:)column([^}]*?\})'
if re.search(css_pattern, html):
    html = re.sub(css_pattern, r'\g<1>row\g<2>', html)
    print("Changed CSS flex-direction to row")
    changed = True

# 3. Change gap from 3px to 6px if it is 3px
css_pattern2 = r'(\.stat-right-group\s*\{[^}]*?gap:)3px([^}]*?\})'
if re.search(css_pattern2, html):
    html = re.sub(css_pattern2, r'\g<1>6px\g<2>', html)
    print("Changed CSS gap to 6px")
    changed = True

if changed:
    with open('tasks.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Done")
else:
    print("No changes made")
