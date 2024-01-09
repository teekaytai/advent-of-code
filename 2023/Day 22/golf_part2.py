import re
D=[(0,E:=set())]*100
t=i=0
for Z,Y,X,z,y,x in sorted([*map(int,re.split('~|,',l))][::-1]for l in open(0)):
 i+=1;m=0;s=E;R=range(10*y+x,10*Y+X+1,9*(Y>y)+1)
 for j in R:h,S=D[j];m>h or(s:=[s&S,S][h>m])<{m:=h}
 for j in R:D[j]=m+Z-z+1,s|{i}
 t+=len(s)
print(t)