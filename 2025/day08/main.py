import math

class UF:
    def __init__(self, n):
        self.pars = list(range(n))
        self.sizes = [1] * n

    def find(self, i):
        if self.pars[i] != i:
            self.pars[i] = self.find(self.pars[i])
        return self.pars[i]

    def union(self, i, j):
        r1 = self.find(i)
        r2 = self.find(j)
        if r1 == r2:
            return False
        self.pars[r1] = r2
        self.sizes[r2] += self.sizes[r1]
        return True

PART1_STEPS = 1000  # Set to 10 for sample input

ps = [tuple(map(int, l.split(','))) for l in open(0)]
n = len(ps)
a = sorted((math.dist(ps[u], ps[v]), u, v) for u in range(n) for v in range(u + 1, n))
uf = UF(n)
merges = 0
for step, (_, u, v) in enumerate(a, start=1):
    merges += uf.union(u, v)
    if step == PART1_STEPS:
        szs = sorted(s for i, s in enumerate(uf.sizes) if uf.pars[i] == i)
        print(szs[-1] * szs[-2] * szs[-3])
    if merges == n - 1:
        print(ps[u][0] * ps[v][0])
        break
