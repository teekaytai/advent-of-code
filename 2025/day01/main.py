x = 50
t1 = 0
t2 = 0
for l in open(0):
    d = int(l[1:])
    t2 += d // 100
    d %= 100
    y = (x + (1 if l[0] == 'R' else -1) * d) % 100
    t1 += y == 0
    t2 += x != 0 and (y == 0 or (y > x) == (l[0] == 'L'))
    x = y
print(t1)
print(t2)
