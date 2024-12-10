DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
g = [list(map(int, l.strip())) for l in open(0)]
h = len(g)
w = len(g[0])
t1 = 0
t2 = 0
for R, row in enumerate(g):
    for C, cell in enumerate(row):
        if cell != 0: continue
        q = [(R,C)]
        for i in range(1, 10):
            q2 = []
            for r, c in q:
                for dr, dc in DIRS:
                    r2 = r + dr
                    c2 = c + dc
                    if 0<=r2<h and 0<=c2<w and g[r2][c2] == i:
                        q2.append((r2,c2))
            q = q2
            if not q: break
        t1 += len(set(q))
        t2 += len(q)
print(t1)
print(t2)
