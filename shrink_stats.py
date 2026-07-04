import re

def shrink_stats():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Change .stat
    old_stat = '.stat { background:var(--bg3); border:1px solid var(--border); border-radius:10px; padding:12px 16px; min-width:100px; text-align:center; flex:1; }'
    new_stat = '.stat { background:var(--bg3); border:1px solid var(--border); border-radius:8px; padding:6px 14px; display:flex; align-items:center; gap:8px; flex:1; min-width:max-content; justify-content:center; }'
    html = html.replace(old_stat, new_stat)

    old_stat_num = '.stat-num { font-size:22px; font-weight:800; }'
    new_stat_num = '.stat-num { font-size:16px; font-weight:800; }'
    html = html.replace(old_stat_num, new_stat_num)

    old_stat_label = '.stat-label { font-size:10px; color:var(--text3); text-transform:uppercase; letter-spacing:.5px; margin-top:2px; }'
    new_stat_label = '.stat-label { font-size:10px; color:var(--text3); text-transform:uppercase; letter-spacing:.5px; margin-top:0; white-space:nowrap; }'
    html = html.replace(old_stat_label, new_stat_label)

    old_compact_stat = '.stats-bar.compact .stat { padding:6px 10px; min-width:70px; border-radius:8px; }'
    new_compact_stat = '.stats-bar.compact .stat { padding:4px 10px; min-width:70px; border-radius:6px; display:flex; align-items:center; gap:6px; flex:1; min-width:max-content; justify-content:center; }'
    html = html.replace(old_compact_stat, new_compact_stat)

    old_compact_num = '.stats-bar.compact .stat-num { font-size:16px; }'
    new_compact_num = '.stats-bar.compact .stat-num { font-size:14px; }'
    html = html.replace(old_compact_num, new_compact_num)

    old_compact_label = '.stats-bar.compact .stat-label { font-size:8px; margin-top:1px; }'
    new_compact_label = '.stats-bar.compact .stat-label { font-size:8px; margin-top:0; white-space:nowrap; }'
    html = html.replace(old_compact_label, new_compact_label)
    
    # Export button
    old_btn_export = '.btn-export { padding:8px 16px; border:1px solid var(--blue); border-radius:8px; background:rgba(108,140,255,0.1);'
    new_btn_export = '.btn-export { padding:6px 14px; border:1px solid var(--blue); border-radius:8px; background:rgba(108,140,255,0.1); display:flex; align-items:center; justify-content:center; height:100%; min-height: 32px;'
    html = html.replace(old_btn_export, new_btn_export)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    shrink_stats()
