a = [tuple(map(int, l.split(','))) for l in open(0)]
xs = sorted({x for x, _ in a})
ys = sorted({y for _, y in a})
n = len(xs)
m = len(ys)
xm = {x: i for i, x in zip(range(0, 2 * n, 2), xs)}
ym = {y: i for i, y in zip(range(0, 2 * m, 2), ys)}
ps = [[0] * (2 * m) for _ in range(2 * n)]
edges = [[] for _ in range(n)]
for i in range(len(a)):
    j = (i + 1) % len(a)
    x, y1 = a[i]
    if a[j][0] != x:
        continue
    y2 = a[j][1]
    edges[xm[x] // 2].append(tuple(sorted((ym[y1], ym[y2]))))
for ei, es in enumerate(edges):
    xi = ei * 2
    for yilo, yihi in es:
        ps[xi + 1][yilo + 1] = 1
        ps[xi + 1][yihi + 1] = 1
for i in range(1, 2 * n):
    for j in range(1, 2 * m):
        ps[i][j] ^= ps[i - 1][j] ^ ps[i][j - 1] ^ ps[i - 1][j - 1]
for i in range(1, 2 * n):
    for j in range(1, 2 * m):
        ps[i][j] += ps[i - 1][j] + ps[i][j - 1] - ps[i - 1][j - 1]

ans1 = 0
ans2 = 0
for i, (x1, y1) in enumerate(a):
    for j in range(i + 1, len(a)):
        x2, y2 = a[j]
        v = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
        ans1 = max(ans1, v)
        xi1, xi2 = sorted((xm[x1], xm[x2]))
        yi1, yi2 = sorted((ym[y1], ym[y2]))
        if ps[xi2][yi2] - ps[xi1][yi2] - ps[xi2][yi1] + ps[xi1][yi1] == (xi2 - xi1) * (yi2 - yi1):
            ans2 = max(ans2, v)
print(ans1)
print(ans2)
