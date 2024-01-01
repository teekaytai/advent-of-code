from heapq import*
V={N:=len(g:=open(x:=0).read())}
q=[(0,0,1,0),(0,0,W:=g.find('\n')+1,0)]
while q:
 t,z,d,c=heappop(q);s=z,d,c
 if{s}-V:V|={s};x=x or(c>3<z>N-3)*t;R=W//d;[heappush(q,(t+int(g[Z]),Z,D,C))for Z,D,C in[(z+d,d,c+1),(z+R,R,1),(z-R,-R,1)][c>9:c//4*2+1]if-1<Z<N>W-Z%W>1]
print(x)