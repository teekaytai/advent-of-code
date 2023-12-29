L=len(g:=[*open(I:=0).read()])
G=g.index
W=G('\n')+1
B=[0]*L
D=[{-W,W},{1,-1},{-W,1},{-W,-1},{W,-1},{1,W},{}]
P='|-LJ7F'
f=lambda z:{z+d for d in D[P.find(g[z])]}
q,*Q=[s:=G('S')],
g[s]=P[D.index({d for d in(-W,1,W,-1)if-1<s+d<L and s in f(s+d)})]
while q:
 for z in q:
  for Z in f(z):Q+=[Z]*-~-B[Z];B[z]=1
 q,*Q=Q,
print(sum(1-b&(I:=I^b&(c in'|LJ'))for c,b in zip(g,B)))