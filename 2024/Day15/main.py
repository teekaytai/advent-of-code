D = dict(zip('^>v<',[(-1,0),(0,1),(1,0),(0,-1)]))
a,b = open(0).read().split('\n\n')
G = list(a.splitlines())

g = [list(l) for l in G]
R, C = next((r, c) for r, row in enumerate(g) for c, cell in enumerate(row) if cell == '@')
g[R][C] = '.'
r, c = R, C
s = ''.join(b.split())
for d in s:
    dr, dc = D[d]
    k = 1
    r2 = r + dr
    c2 = c + dc
    while g[r2][c2] == 'O':
        r2 += dr
        c2 += dc
    if g[r2][c2] == '.':
        g[r2][c2] = 'O'
        r += dr
        c += dc
        g[r][c] = '.'
print(sum(r*100 + c for r, row in enumerate(g) for c, cell in enumerate(row) if cell == 'O'))

g = [[c for cell in row for c in (cell, cell if cell not in 'O@' else '.')] for row in G]
r = R
c = C * 2
g[r][c] = '.'
for d in s:
    dr, dc = D[d]
    if dc:
        c2 = c + dc
        while g[r][c2] == 'O' or g[r][c2-1] == 'O':
            c2 += 2 * dc
        if g[r][c2] == '.':
            for c3 in range(c2, c, -dc):
                g[r][c3] = g[r][c3 - dc]
            c += dc
    else:
        q = [(r, c)]
        seen = set()
        for r1, c1 in q:
            r2 = r1 + dr
            if (r2, c1) in seen: continue
            if g[r2][c1] == '#':
                break
            if g[r2][c1] == 'O' or g[r2][c1-1] == 'O':
                for p in [(r2, c1), (r2, c1-1 if g[r2][c1] != 'O' else c1+1)]:
                    if p not in seen:
                        seen.add(p)
                        q.append(p)
        else:
            for r2, c2 in reversed(q):
                g[r2+dr][c2] = g[r2][c2]
                g[r2][c2] = '.'
            r += dr
print(sum(r*100 + c for r, row in enumerate(g) for c, cell in enumerate(row) if cell == 'O'))
