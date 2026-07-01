import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

with open('tasks.html', 'r', encoding='utf-8') as f:
    tasks_content = f.read()

# Extract top-row and filter-tabs from tasks.html
top_row_match = re.search(r'(<div class="top-row">.*?</div>\s*</div>\s*</div>)', tasks_content, re.DOTALL)
filter_tabs_match = re.search(r'(<div class="filter-tabs">.*?</div>)', tasks_content, re.DOTALL)

if top_row_match and filter_tabs_match:
    top_row_html = top_row_match.group(1)
    filter_tabs_html = filter_tabs_match.group(1)
    
    # We need to change all onclick="function()" to onclick="document.getElementById('iframe-tasks').contentWindow.function()"
    # The functions used in tasks.html top-row and filters are: createTask(), exportExcel(), setFilter('...', this)
    # Actually `setFilter('all', this)` passes `this`. `this` is the button in the parent window.
    # In `tasks.html`'s `setFilter(filterType, btn)`:
    # It does: `document.querySelectorAll('.filter-tab').forEach(b => b.classList.remove('active'));`
    # We will fix `tasks.html` JS to handle this.
    
    combined_html = top_row_html + "\n" + filter_tabs_html
    combined_html = combined_html.replace('onclick="createTask()"', 'onclick="document.getElementById(\'iframe-tasks\').contentWindow.createTask()"')
    combined_html = combined_html.replace('onclick="exportExcel()"', 'onclick="document.getElementById(\'iframe-tasks\').contentWindow.exportExcel()"')
    combined_html = re.sub(r'onclick="setFilter\((.*?)\)"', r'onclick="document.getElementById(\'iframe-tasks\').contentWindow.setFilter(\1)"', combined_html)
    
    # Inject into index.html inside tasks-header-filters
    index_content = index_content.replace(
        '<div id="tasks-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: flex-end; gap: 8px;"></div>',
        f'<div id="tasks-header-filters" class="header-filters" style="flex: 1; display: none; flex-direction: column; align-items: flex-end; justify-content: flex-end; gap: 8px;">\n{combined_html}\n</div>'
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)
        
    print("Updated index.html with tasks controls!")
else:
    print("Could not extract tasks html!")

# 2. Update tasks.html
# Remove the extracted HTML
if top_row_match and filter_tabs_match:
    # We will remove from <!-- TOP ROW: FORM LEFT | STATS RIGHT --> down to the end of <!-- FILTER TABS -->
    # It's easier to just regex out the whole block
    tasks_content = re.sub(r'<!-- TOP ROW: FORM LEFT \| STATS RIGHT -->.*?<!-- END OF FILTER TABS -->', '', tasks_content, flags=re.DOTALL)
    # Wait, I don't have <!-- END OF FILTER TABS -->.
    # I'll just remove the matched strings
    tasks_content = tasks_content.replace(top_row_match.group(1), '')
    tasks_content = tasks_content.replace(filter_tabs_match.group(1), '')
    
    # Also remove <div class="container" style="padding-top:12px;"> ... actually maybe keep it for the rest of the content?
    # No, there is <div class="task-board"> below it. It needs the container.

    # Update JS: Replace document.getElementById(X) with (document.getElementById(X) || window.parent.document.getElementById(X))
    # It's better to add a helper at the top of the <script>
    helper_script = """
const P_DOC = window.parent.document;
function getEl(id) {
    let el = document.getElementById(id);
    if (!el && P_DOC) el = P_DOC.getElementById(id);
    return el;
}
function getEls(selector) {
    let els = document.querySelectorAll(selector);
    if (els.length === 0 && P_DOC) els = P_DOC.querySelectorAll(selector);
    return els;
}
"""
    tasks_content = tasks_content.replace('<script>', f'<script>\n{helper_script}')
    
    # Now replace document.getElementById with getEl
    tasks_content = tasks_content.replace("document.getElementById", "getEl")
    # And replace document.querySelectorAll('.filter-tab') with getEls('.filter-tab')
    tasks_content = tasks_content.replace("document.querySelectorAll('.filter-tab')", "getEls('.filter-tab')")

    with open('tasks.html', 'w', encoding='utf-8') as f:
        f.write(tasks_content)
        
    print("Updated tasks.html successfully!")

