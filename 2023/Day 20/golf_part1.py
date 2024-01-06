g={}
s={}
for l in open(0):
 u,A=l[1:-1].split(' -> ');V=A.split(', ');g[u[:3]]=l[0],V
 for v in V:s[v]={**s.get(v,{}),u:1}
C=[0]*1000
for _ in C:
 q=[(_,1,'roa')]
 for r,p,u in q:
  C[p%2]+=1
  if u in g:
   t,V=g[u];P=('a'<t)*2-1
   if(t<'&')*p:P=s[u]=not s[u]
   if'&'==t:s[u][r]=p;P=1-any(s[u].values())
   if-1<P:q+=[(u,P,v)for v in V]
print(C[0]*C[1])