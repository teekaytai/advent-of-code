import re
H=[[*map(int,re.split(',|@',l))]for l in open(0)]
print(sum(((m:=w/v)!=(M:=W/V))and(p:=(Y-M*X-(c:=y-m*x))/(m-M))>2e14<m*p+c<4e14>p>(p-x)/v>0<V*(p-X)for x,y,_,v,w,_ in H for X,Y,_,V,W,_ in H)//2)