from collections import defaultdict

def f(r1, c1, r2, c2):
    return r2 * 2 - r1, c2 * 2 - c1

d = defaultdict(list)
*g, = map(str.strip, open(0))
n = len(g)
for r, row in enumerate(g):
    for c, cell in enumerate(row):
        if cell != '.':
            d[cell].append((r, c))
s = set()
s2 = set()
for lst in d.values():
    for i, (r1, c1) in enumerate(lst):
        for j in range(i):
            (r2, c2) = lst[j]
            for r3, c3 in f(r1, c1, r2, c2), f(r2, c2, r1, c1):
                if 0 <= r3 < n and 0 <= c3 < n:
                    s.add((r3, c3))
            dr = r2 - r1
            dc = c2 - c1
            r = r1
            c = c1
            while 0 <= r < n > c >= 0:
                r -= dr
                c -= dc
            r += dr
            c += dc
            while 0 <= r < n > c >= 0:
                s2.add((r, c))
                r += dr
                c += dc
print(len(s))
print(len(s2))
