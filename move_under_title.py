import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find the h1 and header-right
pattern = re.compile(
    r'(<h1 style="margin: 0; font-size: 24px; font-weight: 800;">\s*<span[^>]*>.*?</span>\s*</h1>)\s*<div class="header-right" style="display: flex; align-items: center; gap: 20px; margin-left: 20px;">\s*<button id="themeToggle"[^>]*>\s*<span id="themeIcon">.*?</span> Giao diện\s*</button>\s*<div>Cập nhật:.*?</div>\s*</div>',
    re.DOTALL
)

replacement = r'''<div style="display: flex; flex-direction: column; align-items: flex-start; gap: 8px;">
            \1
            <div class="header-right" style="display: flex; align-items: center; gap: 16px; margin-left: 0;">
                <button id="themeToggle" onclick="toggleTheme()" style="background: var(--bg2); border: 1px solid var(--border); color: var(--text); padding: 6px 10px; border-radius: var(--radius); cursor: pointer; font-size: 12px; font-weight: 600; display: flex; align-items: center; gap: 6px; transition: all 0.2s;">
                    <span id="themeIcon">☀️</span> Giao diện
                </button>
                <div style="font-size: 12px; color: var(--text3); font-weight: 500;">Cập nhật: 01/07/2026 14:49</div>
            </div>
        </div>'''

new_content = pattern.sub(replacement, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated successfully!")
