from math import prod

I = open(0).read()
a, *A, B = I.splitlines()
o = B.split()
ts = [int(x) for x in a.split()]
for l in A:
    vs = [int(x) for x in l.split()]
    for i in range(len(ts)):
        ts[i] = ts[i] + vs[i] if o[i] == '+' else ts[i] * vs[i]
print(sum(ts))

g = I.splitlines()
t = 0
xs = []
skip = False
for c in range(max(map(len, g)) - 1, -1, -1):
    if skip:
        skip = False
        continue
    x = 0
    for r in range(len(g) - 1):
        if c < len(g[r]) and g[r][c] != ' ':
            x = x * 10 + int(g[r][c])
    xs.append(x)
    if c < len(g[-1]) and g[-1][c] != ' ':
        t += sum(xs) if g[-1][c] == '+' else prod(xs)
        xs = []
        skip = True
print(t)
