import re
D=[(i:=0,T:=set())]*100
for Z,Y,X,z,y,x in sorted([*map(int,re.split('~|,',l))][::-1]for l in open(0)):
 i+=1;m=0;s=T;R=range(10*y+x,10*Y+X+1,9*(Y>y)+1)
 for j in R:h,k=D[j];m>h or(s:=[s|k,k][h>m])<{m:=h}
 for j in R:D[j]=m+Z-z+1,{i}
 if len(s)<2:T|=s
print(i-len(T))