t=0
t2=0
for l in open(0):
    a=[int(x) for x in l.split()]
    b = [y-x for x,y in zip(a,a[1:])]
    t += all(0<d<4 for d in b) or all(0>d>-4 for d in b)
    for i in range(len(a)):
        a2 = a[:i]+a[i+1:]
        b = [y-x for x,y in zip(a2,a2[1:])]
        if all(0<d<4 for d in b) or all(0>d>-4 for d in b):
            t2 += 1
            break
print(t)
print(t2)
