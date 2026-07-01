with open('index.html', 'rb') as f:
    c = f.read()
print(c.count(b'T\xe1\xbb\x95ng'))
