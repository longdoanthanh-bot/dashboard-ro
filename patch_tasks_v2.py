import re

c = open('tasks.html', 'r', encoding='utf-8').read()

# 1. Modify top-row
c = c.replace('<div class="top-row">', '<div class="top-row" style="position: absolute; top: 10px; right: 10px; z-index: 1000; flex-direction: column; align-items: flex-end; gap: 8px; pointer-events: none; width: max-content; max-width: calc(100% - 20px);">')

# 2. Modify stat-right-group to row
stat_group_idx = c.find('.stat-right-group {')
if stat_group_idx != -1:
    flex_dir_idx = c.find('flex-direction:column;', stat_group_idx)
    if flex_dir_idx != -1 and flex_dir_idx < c.find('}', stat_group_idx):
        c = c[:flex_dir_idx] + 'flex-direction:row;' + c[flex_dir_idx + len('flex-direction:column:'):]

# 3. Add pointer-events: auto to the children
c = c.replace('<div class="add-form">', '<div class="add-form" style="pointer-events: auto;">')
c = c.replace('<div class="stats-row">', '<div class="stats-row" style="pointer-events: auto;">')

# 4. Swap add-form and stats-row
s_add = c.find('<!-- ADD TASK FORM -->')
e_add = c.find('<div class="stats-row"', s_add)
add_block = c[s_add:e_add]

s_stat = e_add
e_stat = c.find('<!-- FILTER TABS -->')
s_tail = c.rfind('</div>', s_stat, e_stat)
stat_block = c[s_stat:s_tail]
tail_block = c[s_tail:e_stat]

new_c = c[:s_add] + stat_block + add_block + tail_block + c[e_stat:]

with open('tasks.html', 'w', encoding='utf-8') as f:
    f.write(new_c)

print("tasks.html patched v2")
