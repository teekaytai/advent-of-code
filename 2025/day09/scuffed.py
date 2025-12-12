from itertools import groupby
from operator import itemgetter

a = sorted(tuple(map(int, l.split(','))) for l in open(0))
xs = sorted({x for x, _ in a})
ys = sorted({y for _, y in a})
# Will fail in some cases since cannot tell if gap present or absent between adjacent coordinates
xm = {x: i for i, x in enumerate(xs)}
ym = {y: i for i, y in enumerate(ys)}
n = len(xs)
m = len(ys)
ps = [[0] * (m + 1) for _ in range(n + 1)]
los = set()
his = set()
for x, g in groupby(a, key=itemgetter(0)):
    xi = xm[x]
    gl = list(g)
    to_remove = []
    for i in range(0, len(gl), 2):
        yilo = ym[gl[i][1]]
        yihi = ym[gl[i + 1][1]]
        if yilo in his:
            his.remove(yilo)
            his.add(yihi)
        elif yihi in los:
            los.remove(yihi)
            los.add(yilo)
        elif yilo not in los and yihi not in his:
            los.add(yilo)
            his.add(yihi)
        else:
            to_remove.append((yilo, yihi))
    starts = sorted(los)
    ends = sorted(his)
    for s, e in zip(starts, ends):
        for yi in range(s, e + 1):
            ps[xi][yi] = 1
    for yilo, yihi in to_remove:
        if yilo in los:
            los.remove(yilo)
            if yihi in his:
                his.remove(yihi)
            else:
                los.add(yihi)
        else:
            his.remove(yihi)
            if yilo in los:
                los.remove(yilo)
            else:
                his.add(yilo)
for i in range(n):
    for j in range(m):
        ps[i][j] += ps[i][j - 1] + ps[i - 1][j] - ps[i - 1][j - 1]

ans1 = 0
ans2 = 0
for i, (x1, y1) in enumerate(a):
    for j in range(i + 1, len(a)):
        x2, y2 = a[j]
        v = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
        ans1 = max(ans1, v)
        xi1, xi2 = sorted((xm[x1], xm[x2]))
        yi1, yi2 = sorted((ym[y1], ym[y2]))
        if ps[xi2][yi2] - ps[xi1 - 1][yi2] - ps[xi2][yi1 - 1] + ps[xi1 - 1][yi1 - 1] == (xi2 - xi1 + 1) * (yi2 - yi1 + 1):
            ans2 = max(ans2, v)
print(ans1)
print(ans2)
