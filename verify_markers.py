import sys
sys.stdout.reconfigure(encoding='utf-8')
markers = ['TONKHO_TBODY_START','TONKHO_TBODY_END','CAL_GRID_START','CAL_GRID_END','STORE_COORDS','TRIP_DATA']
with open('index.html','r',encoding='utf-8-sig') as f:
    c = f.read()
all_ok = True
for m in markers:
    n = c.count(m)
    status = 'OK' if n > 0 else 'MISSING!'
    if n == 0:
        all_ok = False
    print(f'  {m}: {status} ({n})')
print(f'\nAll markers present: {all_ok}')
