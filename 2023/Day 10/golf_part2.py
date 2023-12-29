*g,=open(I:=0).read()
G=g.index
D=[{W:=G('\n')+1,-W},{1,i:=-1},{-W,1},{-W,-1},{W,-1},{1,W},{}]
P='|-LJ7F'
f=lambda z:{z+d for d in D[P.find(g[z])]}
q=Q={s:=G('S')}
g[s]=P[D.index({d for d in(-W,1,W,-1)if-1<s+d<len(g)and s in f(s+d)})]
while Q:q|=Q;Q=set.union(*map(f,Q))-q
print(sum(1-(b:=(i:=i+1)in q)&(I:=I^b&(c in'|LJ'))for c in g))