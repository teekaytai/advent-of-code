*S, I = open(0).read().split('\n\n')
szs = []
shs = []
for s in S:
    szs.append(s.count('#'))
    ls = s.splitlines()[1:]
    sh = [[int(c == '#') for c in l] for l in ls]
    hs = set()
    for _ in range(4):
        hs.add(tuple(sum(b << j for j, b in enumerate(row)) for row in sh))
        hs.add(tuple(sum(b << (2 - j) for j, b in enumerate(row)) for row in sh))
        sh = [[sh[j][2 - i] for j in range(3)] for i in range(3)]
    shs.append(list(hs))

def f(g, n, m, xs, r=0, c=0):
    if sum(xs) == 0:
        return True
    for r in range(r, n - 2):
        temp = g[r:r+3]
        for c in range(c, m - 2):
            for i, x in enumerate(xs):
                if x == 0:
                    continue
                for h in shs[i]:
                    if any((g[r + j] >> c) & h[j] for j in range(3)):
                        continue
                    xs[i] -= 1
                    for j, b in enumerate(h):
                        g[r + j] |= b << c
                    if f(g, n, m, xs, r, c + 1):
                        return True
                    g[r:r+3] = temp
                    xs[i] += 1
        c = 0
    return False

ans = 0
for l in I.splitlines():
    dims, *a = l.split()
    n, m = map(int, dims[:-1].split('x'))
    xs = [int(x) for x in a]
    t = n * m
    if t < sum(sz * x for sz, x in zip(szs, xs)):
        continue
    g = [0] * n
    ans += f(g, n, m, xs)
print(ans)
