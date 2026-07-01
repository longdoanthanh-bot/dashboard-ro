import re
import os

file_path = 'tasks.html'
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change .top-row to flex-direction: column
    content = re.sub(
        r'\.top-row \{ display:flex; gap:10px; margin-bottom:6px; align-items:stretch; \}',
        r'.top-row { display:flex; flex-direction:column; gap:10px; margin-bottom:6px; align-items:stretch; }',
        content
    )

    # Move stats-row ABOVE add-form
    # Extract add-form
    add_form_match = re.search(r'<!-- ADD TASK FORM -->.*?</div>\s*</div>\s*</div>\s*</div>', content, re.DOTALL)
    stats_row_match = re.search(r'<!-- STATS — RIGHT SIDE -->.*?(?=</div>\s*</div>\s*<!-- KANBAN BOARDS -->)', content, re.DOTALL)
    
    if add_form_match and stats_row_match:
        add_form_html = add_form_match.group(0)
        stats_row_html = stats_row_match.group(0)
        
        # We find the top-row div and replace its contents
        top_row_pattern = r'(<div class="top-row">).*?(</div>\s*<!-- KANBAN BOARDS -->)'
        replacement = r'\1\n        ' + stats_row_html + '\n        ' + add_form_html + '\n    \2'
        
        # But maybe it's simpler:
        # Just use order in CSS!
        pass

# Let's just use CSS 'order' property to move stats-row above add-form without fragile HTML regex!
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(
    r'\.top-row \{ display:flex; gap:10px; margin-bottom:6px; align-items:stretch; \}',
    r'.top-row { display:flex; flex-direction:column; gap:10px; margin-bottom:6px; align-items:stretch; }\n.stats-row { order: 1; }\n.add-form { order: 2; }',
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("tasks.html layout fixed using CSS order.")
