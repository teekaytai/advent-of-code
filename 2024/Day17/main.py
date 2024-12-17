a,b,c,_,x = open(0)
a = int(a.split()[-1])
b = int(b.split()[-1])
c = int(c.split()[-1])
x = [int(v) for v in x.split()[1].split(',')]

def run(a, b, c):
    i = 0
    def f(p):
        nonlocal a,b,c
        return [0,1,2,3,a,b,c][p]
    ans = []
    while i < len(x):
        o = x[i]
        p = x[i+1]
        if o == 0:
            a = a >> f(p)
        elif o == 1:
            b ^= p
        elif o == 2:
            b = f(p) % 8
        elif o == 3:
            if a != 0: i = p - 2
        elif o == 4:
            b ^= c
        elif o == 5:
            ans.append(f(p) % 8)
        elif o == 6:
            b = a >> f(p)
        else:
            c = a >> f(p)
        i += 2
    return ans

d1, d2 = [x[i + 1] for i in range(0, len(x), 2) if x[i] == 1]

def dfs(a=0, i=0):
    if i == len(x):
        return a
    a <<= 3
    for m in range(8):
        if a == m == 0: continue
        if (m ^ d1 ^ ((a + m) >> (m ^ d1)) ^ d2) % 8 == x[-i-1]:
            ans = dfs(a + m, i + 1)
            if ans is not None:
                return ans

print(','.join(map(str,run(a, b, c))))
print(dfs())
