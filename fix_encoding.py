import re

def html_entities(text):
    return ''.join(f'&#x{ord(c):04X};' if ord(c) > 127 else c for c in text)

def js_entities(text):
    return ''.join(f'\\u{ord(c):04X}' if ord(c) > 127 else c for c in text)

html_replacements = {
    '>Tổng ST<': f'>{html_entities("Tổng ST")}<',
    '>Tất cả<': f'>{html_entities("Tất cả")}<',
    'placeholder="TÌM KIẾM ST"': f'placeholder="{html_entities("TÌM KIẾM ST")}"',
    'placeholder="Gõ mã ST, Enter để tìm..."': f'placeholder="{html_entities("Gõ mã ST, Enter để tìm...")}"',
    '>LỚN CỠ NÀO<': f'>{html_entities("LỚN CỠ NÀO")}<',
    '>Xuất Excel<': f'>{html_entities("Xuất Excel")}<',
    '>Tính KC<': f'>{html_entities("Tính KC")}<',
    '>ĐO KC: ĐIỂM A<': f'>{html_entities("ĐO KC: ĐIỂM A")}<',
    '>ĐIỂM B<': f'>{html_entities("ĐIỂM B")}<'
}

js_replacements = {
    "'Tất cả'": f"'{js_entities('Tất cả')}'",
    "'Tất cả các loại rổ'": f"'{js_entities('Tất cả các loại rổ')}'"
}

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Apply HTML replacements
for k, v in html_replacements.items():
    c = c.replace(k, v)

# Apply JS replacements
for k, v in js_replacements.items():
    c = c.replace(k, v)

with open('index.html', 'w', encoding='utf-8-sig') as f:
    f.write(c)

print("Entities replaced safely!")
