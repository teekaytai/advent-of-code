g=open(0).read()
L=g.find('\n')+1
D=-L,1,L,-1,0
q=[(1,0,1)]
for u,d,p in q:L=max(L,d);q+=u<len(g)-3and[(v,d+1,u)for z in D if('#'<g[v:=u+z])*(D['^>v<'.find(g[v])]+z)*(v-p)*z]or[]
print(L)