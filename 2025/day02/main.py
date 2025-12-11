import re

t1 = 0
t2 = 0
for l in re.findall(r'\d+-\d+', input()):
    x, y = map(int, l.split('-'))
    for i in range(x, y + 1):
        s = str(i)
        k = len(s)
        if k % 2 == 0 and s[:k//2] * 2 == s:
            t1 += i
        for j in range(1, k):
            if k % j == 0 and s[:j] * (k // j) == s:
                t2 += i
                break
print(t1)
print(t2)
