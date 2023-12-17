import math
a,_,*L=open(0)
d={u:(v[1:4],w[:3])for u,_,v,w in map(str.split,L)}
s=[u for u in d if'B'>u[2]]
p=1
for c in s:
 i=0
 while'Z'>c[2]:c=d[c][a[i%~-len(a)]>'Q'];i+=1
 p=math.lcm(p,i)
print(p)