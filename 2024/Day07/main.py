from functools import reduce
from itertools import product
from operator import add, mul

def f(r, v, a, os):
    return any(reduce((lambda acc, p: p[0](acc, p[1])), zip(o, a), initial=v) == r for o in product(os, repeat=len(a)))

t1 = 0
t2 = 0
o1 = add, mul
o2 = add, mul, lambda x, y: int(f'{x}{y}')
for l in open(0):
    r, v, *a = map(int, l.replace(':', '').split())
    if f(r, v, a, o1):
        t1 += r
        t2 += r
    elif f(r, v, a, o2):
        t2 += r
print(t1)
print(t2)
