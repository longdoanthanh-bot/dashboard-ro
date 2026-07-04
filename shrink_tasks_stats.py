import re

def shrink_tasks():
    with open('tasks.html', 'r', encoding='utf-8') as f:
        tasks = f.read()

    # Change .stat-total-card
    old_total_card = '.stat-total-card {\n    flex:0 0 80px; background:var(--bg3); border:1px solid var(--border); border-radius:8px;\n    padding:6px 8px; display:flex; flex-direction:column; align-items:center; justify-content:center;\n    position:relative; overflow:hidden; transition:background .4s;\n}'
    new_total_card = '.stat-total-card {\n    flex:0 0 auto; background:var(--bg3); border:1px solid var(--border); border-radius:8px;\n    padding:6px 12px; display:flex; flex-direction:row; align-items:center; justify-content:center; gap:8px;\n    position:relative; overflow:hidden; transition:background .4s;\n}'
    tasks = tasks.replace(old_total_card, new_total_card)

    old_total_num = '.stat-total-card .stat-num { font-size:20px; font-weight:900; color:#fff; position:relative; z-index:1; text-shadow:0 1px 3px rgba(0,0,0,0.3); }'
    new_total_num = '.stat-total-card .stat-num { font-size:16px; font-weight:900; color:#fff; position:relative; z-index:1; text-shadow:0 1px 3px rgba(0,0,0,0.3); }'
    tasks = tasks.replace(old_total_num, new_total_num)

    old_total_label = '.stat-total-card .stat-label { font-size:7px; color:rgba(255,255,255,0.8); text-transform:uppercase; letter-spacing:.4px; margin-top:1px; position:relative; z-index:1; font-weight:700; }'
    new_total_label = '.stat-total-card .stat-label { font-size:10px; color:rgba(255,255,255,0.8); text-transform:uppercase; letter-spacing:.4px; position:relative; z-index:1; font-weight:700; }'
    tasks = tasks.replace(old_total_label, new_total_label)
    
    old_total_pct = '.stat-total-card .stat-pct { font-size:8px; color:rgba(255,255,255,0.9); font-weight:700; margin-top:2px; position:relative; z-index:1; }'
    new_total_pct = '.stat-total-card .stat-pct { font-size:10px; color:rgba(255,255,255,0.9); font-weight:700; position:relative; z-index:1; }'
    tasks = tasks.replace(old_total_pct, new_total_pct)

    with open('tasks.html', 'w', encoding='utf-8') as f:
        f.write(tasks)

if __name__ == '__main__':
    shrink_tasks()
