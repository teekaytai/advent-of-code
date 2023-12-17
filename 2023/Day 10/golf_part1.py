g=[*open(i:=0).read()]
G=g.index
W=G('\n')+1
f=lambda z:{z+d for d in[[-W,W],[1,-1],[-W,1],[-W,-1],[W,-1],[1,W],[]]['|-LJ7F'.find(g[z])]}
s=G(S:='S')
q,*Q=[s+d for d in(-W,1,W,-1)if-1<s+d<len(g)and s in f(s+d)],
while q:
 for z in q:
  for Z in f(z):Q+=[Z]*(g[Z]!=S);g[z]=S
 q,*Q=Q,;i+=1
print(i)