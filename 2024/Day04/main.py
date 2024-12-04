*s, = map(str.strip,open(0))
n = len(s)
L = [
    *s,
    *map(''.join, zip(*s)),
    *[''.join(s[j][i+j] for j in range(n-i)) for i in range(n)],
    *[''.join(s[i+j][j] for j in range(n-i)) for i in range(1, n)],
    *[''.join(s[n-j-1][i+j] for j in range(n-i)) for i in range(n)],
    *[''.join(s[n-i-j-1][j] for j in range(n-i)) for i in range(1, n)],
]
print(sum(l.count('XMAS')+l.count('SAMX') for l in L))

t = 0
for r in range(n-2):
    for c in range(n-2):
        w = s[r][c]
        x = s[r][c+2]
        y = s[r+2][c]
        z = s[r+2][c+2]
        if 'X' in (w,x,y,z) or 'A' in (w,x,y,z) or s[r+1][c+1] != 'A': continue
        t += w != z and x != y
print(t)
