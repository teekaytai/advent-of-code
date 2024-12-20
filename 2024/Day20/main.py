dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
g = [list(l.strip()) for l in open(0)]
H = len(g)
W = len(g[0])
R,C = next((r,c) for r, row in enumerate(g) for c, cell in enumerate(row) if cell == 'S')
ER,EC = next((r,c) for r, row in enumerate(g) for c, cell in enumerate(row) if cell == 'E')
d1 = [[1e9]*W for _ in range(H)]
d2 = [[1e9]*W for _ in range(H)]
def f(R, C, d):
    q = [(R,C)]
    d[R][C] = 0
    i=0
    while q:
        q2 = []
        i += 1
        for r,c in q:
            for dr, dc in dirs:
                r2 = r + dr
                c2 = c + dc
                if g[r2][c2] != '#' and d[r2][c2] == 1e9:
                    d[r2][c2] = i
                    q2.append((r2,c2))
        q=q2
f(R,C, d1)
f(ER,EC,d2)
D = d1[ER][EC]
t1 = 0
t2 = 0
for r, row in enumerate(g):
    for c, cell in enumerate(row):
        if cell == '#': continue
        for r2 in range(max(r-20,0), min(r+21,H)):
            for c2 in range(max(c-20,0), min(c+21,W)):
                if g[r2][c2] == '#' or (r,c)==(r2,c2): continue
                d = D-d1[r][c]-d2[r2][c2]-abs(r-r2)-abs(c-c2)
                if abs(r-r2)+abs(c-c2)<=2:
                    t1 += d>=100
                if abs(r-r2)+abs(c-c2)<=20:
                    t2 += d>=100
print(t1)
print(t2)
