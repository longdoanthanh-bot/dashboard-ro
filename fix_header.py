import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Locate the header block
start_header = html.find('<header class="header">')
end_header = html.find('</header>', start_header)

if start_header != -1 and end_header != -1:
    header_html = html[start_header:end_header]
    
    # We need to extract themeToggle button and the update div
    btn_match = re.search(r'<button id="themeToggle".*?</button>', header_html, re.DOTALL)
    update_match = re.search(r'<div[^>]*>Cập nhật:.*?</div>', header_html)
    
    if btn_match and update_match:
        btn_str = btn_match.group(0)
        update_str = update_match.group(0)
        
        # Remove them from their current position
        header_html = header_html.replace(btn_str, '')
        header_html = header_html.replace(update_str, '')
        
        # We also need to remove any trailing whitespace or <div style="margin-left: auto..."> wrapper I might have added
        # Look at the previous wrapper: <div style="margin-left: auto; display: flex; align-items: center; gap: 10px;">
        wrapper_pattern = r'<div style="margin-left: auto; display: flex; align-items: center; gap: 10px;">\s*</div>'
        header_html = re.sub(wrapper_pattern, '', header_html)
        
        # Also remove margin-left: auto; from the button itself since it will now be in a flex container on the right
        btn_str = btn_str.replace('margin-left: auto;', '')
        
        # Add them to the end of the header, as a new child of <header>
        right_group = f'<div style="display: flex; align-items: center; gap: 14px;">\n        {btn_str}\n        {update_str}\n    </div>\n'
        
        new_header = header_html.strip() + '\n    ' + right_group
        html = html[:start_header] + new_header + html[end_header:]
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Header updated")
    else:
        print("Could not find button or update text")
else:
    print("Could not find header")
