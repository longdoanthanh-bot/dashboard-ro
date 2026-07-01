with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Added Content-Type meta tag.")
