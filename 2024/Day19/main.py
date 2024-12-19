from functools import cache

a,_,*b = map(str.strip,open(0))
a = set(a.split(', '))

@cache
def f(x, i, g):
    if i == len(x):
        return 1
    return g(x[i:j] in a and f(x, j, g) for j in range(i + 1, len(x) + 1))

print(sum(f(l,0,any) for l in b))
print(sum(f(l,0,sum) for l in b))
