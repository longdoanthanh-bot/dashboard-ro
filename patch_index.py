import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Storemap
storemap_start = c.find('<div class="main-panel" id="panel-storemap">')
storemap_end = c.find('<div id="nearby-panel"', storemap_start)
if storemap_start != -1 and storemap_end != -1:
    # Add position: relative to panel-storemap
    c = c[:storemap_start] + '<div class="main-panel" id="panel-storemap" style="position: relative;">' + c[storemap_start + len('<div class="main-panel" id="panel-storemap">'):]
    
    # Wrap controls
    storemap_inner_start = c.find('>', storemap_start) + 1
    # We must re-find storemap_end because we modified the string length slightly
    storemap_end = c.find('<div id="nearby-panel"', storemap_inner_start)
    
    wrapper_start = '\n    <div class="top-right-overlay" style="position: absolute; top: 10px; right: 10px; z-index: 1000; display: flex; flex-direction: column; align-items: flex-end; gap: 8px; pointer-events: none;">\n        <div style="pointer-events: auto; display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">\n'
    wrapper_end = '\n        </div>\n    </div>\n'
    
    c = c[:storemap_inner_start] + wrapper_start + c[storemap_inner_start:storemap_end] + wrapper_end + c[storemap_end:]

# 2. Tonkho filter row
# We just need to find the filter-row in panel-tonkho
tonkho_start = c.find('<div class="main-panel active" id="panel-tonkho">')
tonkho_filter_start = c.find('<div class="filter-row">', tonkho_start)
if tonkho_filter_start != -1:
    c = c[:tonkho_filter_start] + '<div class="filter-row" style="justify-content: flex-end;">' + c[tonkho_filter_start + len('<div class="filter-row">'):]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("index.html patched")
