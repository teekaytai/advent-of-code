def f(g, r, c):
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    n = len(g)
    seen = [[[False]*4 for _ in range(n)] for _ in range(n)]
    seen[r][c][0] = True
    d = 0
    while True:
        dr, dc = dirs[d]
        r2 = r + dr
        c2 = c + dc
        if r2 < 0 or r2 >= n or c2 < 0 or c2 >= n:
            break
        if seen[r2][c2][d]:
            return 0
        if g[r2][c2] == '#':
            d = (d + 1) % 4
        else:
            r, c = r2, c2
            seen[r][c][d] = True
    return sum(sum(any(x) for x in row) for row in seen)

*g, = map(list,open(0))
n = len(g)
R, C = next((r, c) for r, row in enumerate(g) for c, cell in enumerate(row) if cell == '^')
print(f(g,R,C))

# Brute force go brrr
t = 0
for r in range(n):
    for c in range(n):
        if g[r][c] == '.':
            temp = g[r][c]
            g[r][c] = '#'
            t += f(g, R, C) == 0
            g[r][c] = temp
print(t)
