from math import prod
import re

a = []
for l in open('input.txt').read().splitlines():
    a.append(tuple(map(int, re.findall(r'-?\d+', l))))

def f(t):
    for x,y,dx,dy in a:
        yield (x+dx*t)%101, (y+dy*t)%103

def s(t):
    a = [0] * 4
    for x,y in f(t):
        if x==50 or y==51: continue
        a[(x>50) + 2*(y>51)] += 1
    return prod(a)

# Initially tried to find tree by measuring when more robots accumulate in bottom half of grid
def c(t):
    a = [0] * 4
    for x,y in f(t):
        if x==50 or y==51: continue
        a[(x>50) + 2*(y>51)] += 1
    return a[2] + a[3] - a[0] - a[1]

def p(t):
    g = [['.'] * 101 for _ in range(103)]
    for x,y in f(t):
        g[y][x] = '█'
    for row in g: print(''.join(row))

# Part 1
print(s(100))

# Happened to notice spike in no. of robots in bottom half starting from 98 seconds and every 103 seconds after that
for t in range(1000):
    if c(t) > 200:
        print(t, c(t))
# p(97)
# print()
# p(98)
# print()
# p(99)
# print()

# Manually inspect the grids to find tree
for t in range(98, 100000, 103):
    p(t)
    print(t)
    input() # Program pauses here, press enter to print out next tree
