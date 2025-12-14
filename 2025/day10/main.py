from fractions import Fraction
from functools import reduce
from itertools import combinations, product

def swap_rows(mat, i, j):
    mat[i], mat[j] = mat[j], mat[i]

def div_row(mat, r, x):
    for c in range(len(mat[r])):
        mat[r][c] /= x

def sub_row(mat, i, j, x):
    for c in range(len(mat[i])):
        mat[i][c] -= mat[j][c] * x

def gauss_jordan(mat):
    mat = [row[:] for row in mat]
    n = len(mat)
    m = len(mat[0]) - 1
    R = 0
    for c in range(m):
        for r in range(R, n):
            if mat[r][c] == 0:
                continue
            swap_rows(mat, R, r)
            div_row(mat, R, mat[R][c])
            for i in range(n):
                if i == R:
                    continue
                sub_row(mat, i, R, mat[i][c])
            R += 1
            break
    return mat

ans1 = 0
ans2 = 0
for l in open(0):
    A, *B, C = l.split()
    A = A.strip('[]')
    a = 0
    for i in range(len(A) - 1, -1, -1):
        a = a * 2 + (A[i] == '#')
    bs = [[int(x) for x in s.strip('()').split(',')] for s in B]
    js = [int(x) for x in C.strip('{}').split(',')]

    # Part 1
    ms = [sum(1 << x for x in b) for b in bs]
    for k in range(len(ms) + 1):
        for com in combinations(ms, k):
            if reduce(int.__xor__, com, 0) == a:
                ans1 += k
                break
        else:
            continue
        break

    # Part 2
    mat = [[Fraction(0)] * (len(bs) + 1) for _ in range(len(A))]
    for i, b in enumerate(bs):
        for x in b:
            mat[x][i] = Fraction(1)
    for i, x in enumerate(js):
        mat[i][-1] = Fraction(x)
    rref = gauss_jordan(mat)
    while all(x == 0 for x in rref[-1]):
        rref.pop()
    n = len(rref)
    m = len(rref[0]) - 1
    pivot_cols = set()
    for r in range(n):
        for c in range(m):
            if rref[r][c] == 0:
                continue
            pivot_cols.add(c)
            break
    free_cols = sorted(set(range(m)) - pivot_cols)
    free_coeffs = [[rref[i][j] for j in free_cols] for i in range(n)]
    mn = 1000000000
    for vs in product(range(0, max(js)), repeat=len(free_cols)):
        t = 0
        for r in range(n):
            s = rref[r][-1] - sum(coeff * v for coeff, v in zip(free_coeffs[r], vs))
            if s.denominator != 1 or s < 0:
                break
            t += int(s)
        else:
            mn = min(mn, t + sum(vs))
    ans2 += mn
print(ans1)
print(ans2)
