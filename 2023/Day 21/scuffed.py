# The abomination that first gave me the right answer for part 2
import sys

DIRS = [1,-1,1j,-1j]
t = 0
grid = [line.strip() for line in sys.stdin]
H = len(grid)
W = len(grid[0])
M = H//2
K = 26501365
def bfs(z):
    c= [1]
    q = [z]
    Q=[]
    even = {z}
    odd =set()
    i=0
    while q:
        for z in q:
            for dz in DIRS:
                Z = z + dz
                if 0<=Z.real<H and 0<=Z.imag<W and Z not in odd and Z not in even and grid[int(Z.real)%H][int(Z.imag)%W]=='.':
                    Q.append(Z)
                    odd.add(Z) if i%2==0 else even.add(Z)
        c.append(len(odd) if i % 2 == 0 else len(even))
        q,Q=Q,[]
        i+=1
    return c

def f(a,b):
    if b >= len(a):
        b -= (b - (len(a)-1) + 1) // 2 * 2
    return a[b]

bt=bfs(H-1+M*1j)
left=bfs(M+0j)
right=bfs(M+(W-1)*1j)
top=bfs(0+M*1j)
br=bfs(H-1+(W-1)*1j)
bl=bfs(H-1+0j)
tl=bfs(0j)
tr=bfs((W-1)*1j)
cen=bfs(M+M*1j)

total = f(cen, K)
r=0
while (h:=r*H+M+1)<=K:
    total += f(bt, K-h)+f(top, K-h)
    total += f(left, K-h)+f(right, K-h)
    if K-h<M+1:
        continue
    d,re = divmod((K - h -M -1),W)
    if d>1:
        total += f(bl, re+W+W) + f(br, re+W+W) + f(tl, re+W+W) + f(tr, re+W+W)
        d-=1
    if d>0:
        total += f(bl, re+W) + f(br, re+W) + f(tl, re+W) + f(tr, re+W)
        d-=1
    total += (f(bl,K-h-M-1)*((d+1)//2)+f(bl,K-h-M-1-W)*(d//2))*4 +f(bl, re) + f(br, re) + f(tl, re) + f(tr, re)
    r+=1
print(total)
