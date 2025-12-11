A, B = open(0).read().split('\n\n')
a = sorted(tuple(map(int, l.split('-'))) for l in A.split())

t1 = 0
for x in map(int, B.split()):
    t1 += any(l <= x <= r for l, r in a)
print(t1)

t2 = 0
pr = -1
for l, r in a:
    l = max(l, pr + 1)
    t2 += max(r - l + 1, 0)
    pr = max(pr, r)
print(t2)
