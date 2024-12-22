from collections import Counter
from functools import reduce

a = [int(l) for l in open(0).read().splitlines()]
def f(x):
    for _ in range(2000):
        x = (x ^ (x << 6)) % 16777216
        x = (x ^ (x >> 5)) % 16777216
        x = (x ^ (x << 11)) % 16777216
    return x
def g(x):
    C = Counter()
    a = b = c = d = 0
    for i in range(2000):
        y = (x ^ (x << 6)) % 16777216
        y = (y ^ (y >> 5)) % 16777216
        y = (y ^ (y << 11)) % 16777216
        a, b, c, d, x = b, c, d, y%10 - x%10, y
        if i >= 3 and (a,b,c,d) not in C:
            C[(a,b,c,d)] = y % 10
    return C

print(sum(f(x) for x in a))
print(reduce(Counter.__iadd__, map(g, a)).most_common(1)[0][1])
