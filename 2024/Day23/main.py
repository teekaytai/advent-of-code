from collections import defaultdict

g = defaultdict(set)
for l in open(0).read().splitlines():
    u,v = l.split('-')
    g[u].add(v)
    g[v].add(u)
t = 0
for u, adj in g.items():
    for v in adj:
        for w in adj:
            if v == w: continue
            if w in g[v]:
                t += any(x.startswith('t') for x in [u,v,w])
print(t // 6)

mx = 0
p = set()
def f(s, u):
    global mx, p
    if len(s) > mx:
        mx = len(s)
        p = {*s}
    for v in g[u]:
        if v > u and all(v in g[w] for w in s):
            s.add(v)
            f(s, v)
            s.remove(v)
for u in g: f({u}, u)
print(','.join(sorted(p)))
