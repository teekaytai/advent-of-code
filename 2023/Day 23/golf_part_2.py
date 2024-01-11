g=open(0).read()
S={W:=g.find('\n')+1}
s=[(1,0)*2]
G=[[]for _ in g]
while s:
 u,d,p,c=s.pop()
 if u>len(g)-4:L+=d;e=c;continue
 if len(V:=[u+z for z in(-W,1,W,-1)if'#'<g[u+z]])>2:
  if c:G[c]+=(u,d),;G[u]+=(c,d),
  else:L=d;b=u
  c=u;d=0
 if{u}-S:S|={u};s+=[(v,d+1,u,c)for v in V if v-p]
s=[(b,{b},L)]
while s:u,S,d=s.pop();L=max(L,d*(u==e));s+=[(v,S|{v},d+w)for v,w in G[u]if{v}-S]
print(L)