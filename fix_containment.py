import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Find tasks-header-filters
start = c.find('<div id="tasks-header-filters"')
# Find the exact string we want to remove:
# </div>
#   
#     <!-- FILTER TABS -->
# We know stats_row was inserted. The end of stats_row is </div>\n          </div>\n      </div>
# Wait, let's just find the precise string "      </div>\n  \n      <!-- FILTER TABS -->"
# and remove "      </div>\n  \n      <!-- FILTER TABS -->"
# Actually, the comment <!-- FILTER TABS --> might be useful to remove too since it makes no sense here.
target_to_remove = "</div>\n  \n      <!-- FILTER TABS -->"
if target_to_remove in c:
    c = c.replace(target_to_remove, "")
else:
    # try a regex to find the closing div of tasks-header-filters before filter tabs
    m = re.search(r'</div>\s*<!-- FILTER TABS -->', c)
    if m:
        c = c[:m.start()] + c[m.end():]

# Now tasks-header-filters remains open, absorbing add-form.
# We need to close it after add-form.
# Find the end of add-form block:
add_form_start = c.find('<div class="add-form">', start)
# The add-form block ends with: style="margin-left:4px;">📥 Excel</button>\n          </div>
excel_btn = "Excel</button>\n          </div>"
excel_idx = c.find(excel_btn, add_form_start)
if excel_idx != -1:
    insert_pos = excel_idx + len(excel_btn)
    c = c[:insert_pos] + "\n      </div>" + c[insert_pos:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed tasks-header-filters containment!")
