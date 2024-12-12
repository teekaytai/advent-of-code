DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
g = list(list(l.strip()) for l in open(0))
n = len(g)

def is_in(r, c, cell):
    return 0 <= r < n > c >= 0 and g[r][c] == cell

seen = [[False] * n for _ in range(n)]
t1 = 0
t2 = 0
for R, row in enumerate(g):
    for C, cell in enumerate(row):
        if seen[R][C]: continue
        s = [(R, C)]
        seen[R][C] = True
        a = 1
        p1 = 0
        p2 = 0
        while s:
            r, c = s.pop()
            for dr, dc in DIRS:
                r2 = r + dr
                c2 = c + dc
                if is_in(r2, c2, cell) and not seen[r2][c2]:
                    s.append((r2, c2))
                    seen[r2][c2] = True
                    a += 1
                if not is_in(r2, c2, cell):
                    p1 += 1
                    r3 = r + dc
                    c3 = c - dr
                    r4 = r3 + dr
                    c4 = c3 + dc
                    if not (is_in(r3, c3, cell) and not is_in(r4, c4, cell)):
                        p2 += 1
        t1 += a * p1
        t2 += a * p2
print(t1)
print(t2)
