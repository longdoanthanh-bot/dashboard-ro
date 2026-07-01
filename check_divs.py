import re
c = open('tasks.html', encoding='utf-8').read()
top = c[c.find('<div class="top-row"'):c.find('<!-- KANBAN BOARD -->')]
print("Tasks html top-row div balance:", len(re.findall(r'<div', top)) - len(re.findall(r'</div', top)))
