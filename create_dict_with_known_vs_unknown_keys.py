 = {}

for i in range(3):
    key = i
    value = [i, i*2, i*3]
    if key in d:
        d[key].extend(value)
    else:
        d[key] = value

print(d)



keys = [1, 2, 3]
d = {key: [] for key in keys}

for i in range(3):
    key = i + 1
    value = [i, i*2, i*3]
    d[key].extend(value)

print(d)
