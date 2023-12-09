a,_,*L=open(i:=0)
d={u:(v[1:4],w[:3])for u,_,v,w in map(str.split,L)}
c='AAA'
while'ZZZ'!=c:c=d[c][a[i%(len(a)-1)]>'Q'];i+=1
print(i)