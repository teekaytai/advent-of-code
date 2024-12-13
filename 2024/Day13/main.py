# Uhh... no commemt
from math import gcd
import re

def bezout(x, y):
    if x == 0 or y == 0:
        if x + y != 1: return 0, 0
        return (1, 0) if x else (0, 1)
    t = 0
    i = 0
    j = 0
    while t != 1:
        while t < 1:
            if x > 0: t += x; i += 1
            else: t -= x; i -= 1
        while t > 1:
            if y < 0: t += y; j += 1
            else: t -= y; j -= 1
    return i, j

a = open(0).read().split('\n\n')
t = 0
t2 = 0
for l in a:
    x1, y1, x2, y2, X, Y = map(int, re.findall(r'\d+', l))
    i = (X + x1 - 1) // x1
    j = 0
    x = x1 * i
    y = y1 * i
    m = INF = 1e9
    while i >= 0:
        if x == X and y == Y:
            t += i*3 + j
            break
        i -= 1
        x -= x1
        y -= y1
        while x < X and y < Y:
            x += x2
            y += y2
            j += 1

    X += 10000000000000
    Y += 10000000000000
    d1 = x1 - y1
    d2 = x2 - y2
    D = X - Y
    if d1 + d2 != 0:
        q, r = divmod(D, d1 + d2)
        d = 0
        g = gcd(d1, d2)
        if r % g: continue
        i, j = bezout(d1//g, d2//g)
        if i == j == 0: continue
        i *= r//g
        j *= r//g
        x = d2//g * x1 - d1//g * x2
        y = d2//g * y1 - d1//g * y2
        X -= (i + q) * x1 + (j + q) * x2
        if X % x: continue
        m = X // x
        t2 += 3*(i+q+d2//g*m)+j+q-d1//g*m
    else:
        if D % d1: continue
        q = D // d1
        X -= q * x1
        x = x1 + x2
        if X % x: continue
        m = X // x
        t2 += 3*(m+q) + m
print(t)
print(t2)
