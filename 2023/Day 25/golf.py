C={}
for l in open(0):
 for v in l.split()[1:]:C[u]=C.get(u:=l[:3],{})|{v:1};C[v]=C.get(v,{})|{u:1}
*_,s=C
for t in C:
 for _ in[c:={u:{**C[u]}for u in C}]*4:
  P={};q=[s]
  for u in q:
   for v in c[u]:
    if~-(v in P)*c[u][v]:P[v]=u;q+=[v]
  if{v:=t}-{*P}:L=len(P);print(L*(len(C)-L));quit()
  while v!=s:c[p:=P[v]][v]-=1;c[v][v:=p]+=1