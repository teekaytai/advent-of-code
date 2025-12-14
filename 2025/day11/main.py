from collections import Counter, defaultdict

g = {}
indegs = Counter()
for l in open(0):
    u, *vs = l.split()
    u = u[:-1]
    g[u] = vs
    for v in vs:
        indegs[v] += 1
dp = defaultdict(lambda: [0, 0, 0, 0])
dp['you'] = [1, 0, 0, 0]
dp['svr'] = [0, 1, 0, 0]
s = [u for u in g if u not in indegs]
while s:
    u = s.pop()
    x = dp[u]
    if u in ('dac', 'fft'):
        x[3] = x[2]
        x[2] = x[1]
    if u not in g:
        continue
    for v in g[u]:
        for i in range(4):
            dp[v][i] += x[i]
        indegs[v] -= 1
        if indegs[v] == 0:
            s.append(v)
print(dp['out'][0])
print(dp['out'][3])
