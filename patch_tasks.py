import re

with open('tasks.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Modify top-row
top_row_start = c.find('<div class="top-row">')
c = c[:top_row_start] + '<div class="top-row" style="position: absolute; top: 10px; right: 10px; z-index: 1000; flex-direction: column; align-items: flex-end; gap: 8px;">' + c[top_row_start + len('<div class="top-row">'):]

# 2. Modify stat-right-group to row
stat_group_idx = c.find('.stat-right-group {')
if stat_group_idx != -1:
    flex_dir_idx = c.find('flex-direction:column;', stat_group_idx)
    if flex_dir_idx != -1 and flex_dir_idx < c.find('}', stat_group_idx):
        c = c[:flex_dir_idx] + 'flex-direction:row;' + c[flex_dir_idx + len('flex-direction:column:'):]

# 3. Swap add-form and stats-row
# find add-form block
add_form_start = c.find('<!-- ADD TASK FORM -->\n        <div class="add-form">')
if add_form_start == -1:
    add_form_start = c.find('<!-- ADD TASK FORM -->\r\n        <div class="add-form">')
# the block ends where stats-row begins
stats_row_start = c.find('<div class="stats-row">')

add_form_block = c[add_form_start:stats_row_start]

# stats-row block ends before </div>\n    \n    <!-- FILTER TABS -->
filter_tabs_start = c.find('<!-- FILTER TABS -->')
stats_row_end_match = re.search(r'</div>\s*<!-- FILTER TABS -->', c)

stats_row_block = c[stats_row_start:stats_row_end_match.start()]
stats_row_block = stats_row_block.rstrip()
if stats_row_block.endswith('</div>'):
    # The last </div> belongs to top-row, so don't include it in the swap!
    stats_row_block = stats_row_block[:-6].rstrip()

# Wait, let's just do it cleanly:
c = open('tasks.html', 'r', encoding='utf-8').read() # reload pristine
c = c.replace('<div class="top-row">', '<div class="top-row" style="position: absolute; top: 10px; right: 10px; z-index: 1000; flex-direction: column; align-items: flex-end; gap: 8px;">')
c = c.replace('flex-direction:column;', 'flex-direction:row;') # affects stat-right-group

# swap the two blocks using regex
pattern = re.compile(r'(<!-- ADD TASK FORM -->\s*<div class="add-form">.*?</button>\s*</div>\s*)(<div class="stats-row">.*?</div>\s*</div>\s*</div>)', re.DOTALL)
m = pattern.search(c)
if m:
    add_form_block = m.group(1)
    stats_row_block = m.group(2)
    # Actually, stats_row_block contains the closing </div> for top-row.
    # We should keep the closing </div> at the end.
    # stats_row_block ends with </div>\n        </div>\n    </div>
    # Let's write a safer replace
    pass

c = open('tasks.html', 'r', encoding='utf-8').read() # reload pristine
c = c.replace('<div class="top-row">', '<div class="top-row" style="position: absolute; top: 10px; right: 10px; z-index: 1000; flex-direction: column; align-items: flex-end; gap: 8px; pointer-events: none;">')
# add pointer-events: auto to the children
c = c.replace('<div class="add-form">', '<div class="add-form" style="pointer-events: auto;">')
c = c.replace('<div class="stats-row">', '<div class="stats-row" style="pointer-events: auto;">')
c = c.replace('flex-direction:column;', 'flex-direction:row;')

# Instead of regex, split and re-assemble
# Extract add-form
s_add = c.find('<!-- ADD TASK FORM -->')
e_add = c.find('<div class="stats-row"', s_add)
add_block = c[s_add:e_add]

# Extract stats-row
s_stat = e_add
e_stat = c.find('<!-- FILTER TABS -->')
# We need to find the closing div of top-row which is right before <!-- FILTER TABS -->
# Let's take up to the last </div> before FILTER TABS
s_tail = c.rfind('</div>', s_stat, e_stat)
stat_block = c[s_stat:s_tail]
tail_block = c[s_tail:e_stat]

new_c = c[:s_add] + stat_block + add_block + tail_block + c[e_stat:]

with open('tasks.html', 'w', encoding='utf-8') as f:
    f.write(new_c)

print("tasks.html patched")
