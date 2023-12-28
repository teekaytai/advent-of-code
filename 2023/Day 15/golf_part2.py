d={}
for p in input().split(','):
 d.pop(p[:-1],b:=[t:=0]*256)
 if'='in p:d[p[:-2]]=int(p[-1])
for s in d:h=0;[h:=17*(h+ord(c))%256for c in s];b[h]+=1;t+=(h+1)*b[h]*d[s]
print(t)