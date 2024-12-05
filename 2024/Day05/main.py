from collections import defaultdict
from functools import cmp_to_key

A,B = open(0).read().strip().split('\n\n')
d = defaultdict(set)
for l in A.split('\n'):
    x,y = map(int,l.split('|'))
    d[x].add(y)
t = 0
t2 = 0
for l in B.split('\n'):
    *a, = map(int,l.split(','))
    can = True
    for i, x in enumerate(a):
        for j in range(i):
            if x not in d[a[j]]:
                can = False
                break
        if not can:
            break
    if can:
        t += a[len(a)//2]
    else:
        a.sort(key=cmp_to_key(lambda x, y: -1 if y in d[x] else 1 if x in d[y] else 0))
        t2 += a[len(a)//2]
print(t)
print(t2)
