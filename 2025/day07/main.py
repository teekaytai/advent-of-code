from collections import Counter

a, *I = open(0).readlines()
c = Counter({a.find('S'): 1})
t = 0
for l in I:
    c2 = Counter()
    for i, x in enumerate(l):
        if x == '^' and i in c:
            c2[i - 1] += c[i]
            c2[i + 1] += c[i]
            del c[i]
            t += 1
    c += c2
print(t)
print(c.total())
