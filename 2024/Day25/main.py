a = open(0).read().split('\n\n')
ks = []
ls = []
for x in a:
    x = [l.strip() for l in x.splitlines()]
    if x[0] == '#####':
        b = []
        for i in range(5):
            for j in range(7):
                if x[j][i] == '.': break
            b.append(j-1)
        ks.append(b)
    else:
        b = []
        for i in range(5):
            for j in range(7):
                if x[j][i] == '#': break
            b.append(6-j)
        ls.append(b)
t = 0
for k in ks:
    for l in ls:
        if all(x+y<6 for x, y in zip(k, l)): t += 1
print(t)
