dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
dirs2 = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

class UF:
    def __init__(self, n):
        self.pars = list(range(n))

    def find(self, i):
        if self.pars[i] != i:
            self.pars[i] = self.find(self.pars[i])
        return self.pars[i]

    def union(self, i, j):
        self.pars[self.find(i)] = self.find(j)

a = [tuple(map(int, l.split(','))) for l in open(0).readlines()]
n = 71

m = 1028
g = [[False] * n for _ in range(n)]
for c, r in a[:m]:
    g[r][c] = True
q = [(0, 0)]
i = 0
while not g[n-1][n-1]:
    i += 1
    q2 = []
    for r, c in q:
        for dr, dc in dirs:
            r2 = r + dr
            c2 = c + dc
            if 0<=r2<n>c2>=0 and not g[r2][c2]:
                g[r2][c2] = True
                q2.append((r2, c2))
    q = q2
print(i)

g = [[False] * n for _ in range(n)]
uf = UF(n*n+2)
s = n*n
t = s + 1
for i, (c, r) in enumerate(a):
    g[r][c] = True
    if r == 0 or c == n-1:
        uf.union(r*n+c,s)
    if r == n-1 or c == 0:
        uf.union(r*n+c,t)
    for dr, dc in dirs2:
        r2 = r + dr
        c2 = c + dc
        if 0<=r2<n>c2>=0 and g[r2][c2]:
            uf.union(r*n+c,r2*n+c2)
    if uf.find(s) == uf.find(t):
        break
print(*a[i], sep=',')
