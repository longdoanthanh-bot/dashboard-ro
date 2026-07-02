import re

def horizontal_layout():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update top-controls for Tonkho
    # Change top-controls style
    html = html.replace(
        'class="top-controls" style="display: flex; flex-direction: column; align-items: flex-end; padding-left: 450px;',
        'class="top-controls" style="display: flex; flex-direction: row; align-items: flex-start; justify-content: flex-start; padding-left: 420px; flex-wrap: wrap;'
    )
    # Change filters-container style
    html = html.replace(
        'class="filters-container" style="display: flex; flex-direction: column; align-items: flex-end;',
        'class="filters-container" style="display: flex; flex-direction: row; align-items: center; flex-wrap: wrap;'
    )
    # Remove justify-content: flex-end from filter-row
    html = html.replace(
        '<div class="filter-row" style="margin-bottom: 0; justify-content: flex-end;">',
        '<div class="filter-row" style="margin-bottom: 0; justify-content: flex-start;">'
    )
    
    # 2. Update top-controls-thuhoi for Thuhoi
    html = html.replace(
        'class="top-controls-thuhoi" style="display: flex; flex-direction: column; align-items: flex-end; padding-left: 450px;',
        'class="top-controls-thuhoi" style="display: flex; flex-direction: row; align-items: flex-start; justify-content: flex-start; padding-left: 420px; flex-wrap: wrap;'
    )
    html = html.replace(
        'class="filters-container-thuhoi" style="display: flex; flex-direction: column; align-items: flex-end;',
        'class="filters-container-thuhoi" style="display: flex; flex-direction: row; align-items: center; flex-wrap: wrap;'
    )

    # 3. Update map-controls for Storemap
    html = html.replace(
        'class="map-controls" style="display: flex; flex-direction: column; align-items: flex-end; padding-left: 450px;',
        'class="map-controls" style="display: flex; flex-direction: row; align-items: flex-start; justify-content: flex-start; padding-left: 420px; flex-wrap: wrap;'
    )
    html = html.replace(
        'class="map-controls-right" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-end; justify-content: flex-end;">',
        'class="map-controls-right" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: center; justify-content: flex-start;">'
    )
    html = html.replace(
        'class="map-controls-left" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-end;">',
        'class="map-controls-left" style="display: flex; gap: 12px; flex-wrap: wrap; align-items: center; justify-content: flex-start;">'
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # 4. Update tasks.html
    with open('tasks.html', 'r', encoding='utf-8') as f:
        tasks = f.read()
    
    tasks = tasks.replace(
        'class="top-row" style="display: flex; flex-direction: column; align-items: flex-end; padding-left: 450px;',
        'class="top-row" style="display: flex; flex-direction: row; align-items: flex-start; justify-content: flex-start; padding-left: 420px; flex-wrap: wrap;'
    )
    
    with open('tasks.html', 'w', encoding='utf-8') as f:
        f.write(tasks)

if __name__ == '__main__':
    horizontal_layout()
