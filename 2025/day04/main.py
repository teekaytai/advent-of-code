DIRS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

g = [list(l) for l in map(str.strip, open(0))]
n = len(g)
m = len(g[0])
cs = [[0] * m for _ in range(n)]
st = []
for r, row in enumerate(g):
    for c, x in enumerate(row):
        if x != '@':
            continue
        s = 0
        for dr, dc in DIRS:
            r2 = r + dr
            c2 = c + dc
            if r2 < 0 or r2 >= n or c2 < 0 or c2 >= m:
                continue
            s += g[r2][c2] == '@'
        cs[r][c] = s
        if s < 4:
            st.append((r, c))

t = len(st)
print(t)

for r, c in st:
    g[r][c] = '.'
while st:
    r, c = st.pop()
    for dr, dc in DIRS:
        r2 = r + dr
        c2 = c + dc
        if r2 < 0 or r2 >= n or c2 < 0 or c2 >= m or g[r2][c2] == '.':
            continue
        cs[r2][c2] -= 1
        if cs[r2][c2] < 4:
            g[r2][c2] = '.'
            st.append((r2, c2))
            t += 1
print(t)
