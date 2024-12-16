from heapq import *

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
g = [list(l.strip()) for l in open(0)]
H = len(g)
W = len(g[0])
R = H - 2
C = 1
ts = [[[1e9] * 4 for _ in range(W)] for _ in range(H)]
dp = [[[set()] * 4 for _ in range(W)] for _ in range(H)]
ts[R][C][0] = 0
dp[R][C][0] = {(R, C)}
pq = [(0, R, C, 0)]
while pq:
    t, r, c, d = heappop(pq)
    if t > ts[r][c][d]: continue
    if r == 1 and c == W - 2:
        print(t)
        print(len(dp[r][c][d]))
        break
    for d2, (dr, dc) in enumerate(dirs):
        r2 = r + dr
        c2 = c + dc
        t2 = t + 1 + 1000*(min((d-d2)%4, (d2-d)%4))
        if g[r2][c2] == '#' or t2 > ts[r2][c2][d2]:
            continue
        if t2 == ts[r2][c2][d2]:
            dp[r2][c2][d2] |= dp[r][c][d]
        else:
            ts[r2][c2][d2] = t2
            dp[r2][c2][d2] = dp[r][c][d] | {(r2, c2)}
            heappush(pq, (t2, r2, c2, d2))
