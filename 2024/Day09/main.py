from itertools import accumulate
from heapq import *

*a, = map(int, input())

b = []
for i, v in enumerate(a):
    b += [i//2] * v if i % 2 == 0 else [-1] * v
l = 0
r = len(b) - 1
while l < r:
    while b[l] != -1: l += 1
    while b[r] == -1: r -= 1
    if l > r:
        break
    b[l], b[r] = b[r], b[l]
    l += 1
    r -= 1
print(sum(i * v if v != -1 else 0 for i, v in enumerate(b)))

ans = []
c = list(accumulate(a, initial=0))
d = [[] for _ in range(10)]
for v, i in zip(a[1::2], c[1::2]):
    d[v].append(i)
for i in range(len(a) - (2 - len(a) % 2), -1, -2):
    v, k = a[i], c[i]
    j = min((j for j in range(v, len(d)) if d[j]), key=lambda j: d[j][0], default=-1)
    if j != -1 and d[j][0] < k:
        k = heappop(d[j])
        s = j - v
        if s > 0:
            heappush(d[s], k + v)
    ans.append((k, v, i//2))
print(sum(sum(j*i for j in range(k, k+v)) for k, v, i in ans))
