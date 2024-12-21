from itertools import pairwise, product

a = [l for l in map(str.strip,open(0).readlines())]
vs = [int(l[:-1]) for l in a]

P = dict(zip('0123456789A',[(3,1),(2,0),(2,1),(2,2),(1,0),(1,1),(1,2),(0,0),(0,1),(0,2),(3,2)]))
D = dict(zip(product('<v>^A',repeat=2), range(25)))

m = ['A', '>A', '>>A', '>^A', '>>^A',
     '<A', 'A', '>A', '^A', '^>A',
     '<<A', '<A', 'A', '<^A', '^A',
     'v<A', 'vA', 'v>A', 'A', '>A',
     'v<<A', '<vA', 'vA', '<A', 'A']
M = [[0]*25 for _ in range(25)]
for i, x in enumerate(m):
    for t in pairwise('A'+x):
        M[D[t]][i] += 1

def g(l):
    b = [0] * 25
    s = 'A'
    for p1, p2 in pairwise(map(P.get, 'A'+l)):
        r1 , c1 = p1
        r2 , c2 = p2
        dr = r2 - r1
        dc = c2 - c1
        rr = '^v'[dr>0]*abs(dr)
        cc = '<>'[dc>0]*abs(dc)
        if r1 == 3 and c2 == 0 or not (c1 == 0 and r2 == 3) and (dr < 0 and dc > 0 or dr > 0 and dc > 0):
            s += rr+cc+'A'
        else:
            s += cc+rr+'A'
    for i in map(D.get, pairwise(s)):
        b[i] += 1
    return b

def matmul(A, B):
    ans = [[0] * len(B[0]) for _ in range(len(A))]
    for r, R in enumerate(A):
        for k, va in enumerate(R):
            if not va: continue
            for c, vb in enumerate(B[k]):
                ans[r][c] = (ans[r][c] + va * vb)
    return ans

def matpow(M, p):
    n = len(M)
    ans = [[0] * n for _ in range(n)]
    for i in range(n):
        ans[i][i] = 1
    while p:
        if p & 1:
            ans = matmul(ans, M)
        M = matmul(M, M)
        p >>= 1
    return ans

def f(l, k):
    t = 0
    b = [[x] for x in g(l)]
    t += sum(x for [x] in matmul(matpow(M, k), b))
    return t

print(sum(f(l, 2)*v for l,v in zip(a,vs)))
print(sum(f(l, 25)*v for l,v in zip(a,vs)))


# ¯\_(ツ)_/¯

# Q = dict(zip('<v>^A',[(1,0),(1,1),(1,2),(0,1),(0,2)]))

# def g(p1, p2):
#     r1, c1 = p1
#     r2, c2 = p2
#     dr = r2 - r1
#     dc = c2 - c1
#     if dr == 0 and dc == 0: return ['A']
#     if dr == 0: return ['<>'[dc>0]*abs(dc)+'A']
#     if dc == 0: return ['^v'[dr>0]*abs(dr)+'A']
#     paths = []
#     if not (c1 == 0 and r2 == 3):
#         paths.append('^v'[dr>0]*abs(dr) + '<>'[dc>0]*abs(dc) + 'A')
#     if not (r1 == 3 and c2 == 0):
#         paths.append('<>'[dc>0]*abs(dc) + '^v'[dr>0]*abs(dr) + 'A')
#     return paths

# def h(p1, p2):
#     r1, c1 = p1
#     r2, c2 = p2
#     dr = r2 - r1
#     dc = c2 - c1
#     if dr == 0 and dc == 0: return ['A']
#     if dr == 0: return ['<>'[dc>0]*abs(dc)+'A']
#     if dc == 0: return ['^v'[dr>0]*abs(dr)+'A']
#     paths = []
#     if not (c1 == 0 and r2 == 0):
#         paths.append('^v'[dr>0]*abs(dr) + '<>'[dc>0]*abs(dc) + 'A')
#     if not (r1 == 0 and c2 == 0):
#         paths.append('<>'[dc>0]*abs(dc) + '^v'[dr>0]*abs(dr) + 'A')
#     return paths

# def adj(s, i=0):
#     if i == 2:
#         return len(s)
#     b = [h(Q[p1],Q[p2]) for p1,p2 in pairwise('A'+s)]
#     mn = 1e9
#     for s2a in product(*b):
#         s2 = ''.join(s2a)
#         mn = min(mn, adj(s2, i+1))
#     return mn

# def f(l):
#     o = [P[c] for c in 'A'+l]
#     b = [g(p1,p2) for p1,p2 in pairwise(o)]
#     return(sum(min(adj(s) for s in ss) for ss in b))

# print(sum(f(l)*v for l,v in zip(a,vs)))
