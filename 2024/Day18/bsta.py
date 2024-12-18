dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

a = [tuple(map(int, l.split(','))) for l in open(0).readlines()]
n = 71

def f(m):
    g = [[False] * n for _ in range(n)]
    for c, r in a[:m]:
        g[r][c] = True
    q = [(0, 0)]
    i = 0
    while q:
        i += 1
        q2 = []
        for r, c in q:
            for dr, dc in dirs:
                r2 = r + dr
                c2 = c + dc
                if 0<=r2<n>c2>=0 and not g[r2][c2]:
                    if r2 == n-1 and c2 == n-1:
                        return i
                    g[r2][c2] = True
                    q2.append((r2, c2))
        q = q2
    return 0

print(f(1028))

# Yeah, not sure why I thought of using Union Find before plain ol' binary search
lo = 1
hi = len(a)
while lo < hi:
    mid = (lo + hi) // 2
    if f(mid): lo = mid + 1
    else: hi = mid
print(*a[lo-1], sep=',')

# or even just brute forcing actually (only takes half a second!)
# i = 1
# while f(i): i += 1
# print(*a[i-1], sep=',')
