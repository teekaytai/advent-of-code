import re
a,b,*H=[[*map(int,re.split(',|@',l))]for l in open(0)]
R=0,1,2
s={0}
for i in R:
 for h in H:
  if{p:=h[i]}&s:k=i;P=p;V=h[3+i]
  s|={p}
t=(a[k]-P)//(V-a[3+k])
T=(b[k]-P)//(V-b[3+k])
print(sum((q:=a[i]+a[3+i]*t)-(b[i]+b[3+i]*T-q)*t//(T-t)for i in R))