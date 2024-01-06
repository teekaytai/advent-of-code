g={}
T={}
for l in open(0):v,A=l[1:-1].split(' -> ');g[v[:3]]=A.split(', ');T[v]=l[0]>'%'
p=1
for v in g['roa']:
 r=0;b=1
 while~-T[v]:v,*_,c=sorted(g[v]*2,key=T.get);r|=b*T[c];b*=2
 p*=r
print(p)