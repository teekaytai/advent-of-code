s,b,*L=map(str.split,open(0))
a,*c=[(p:=int(x),p+int(y))for x,y in zip(s[1::2],s[2::2])],
for l in L:
 if len(l)<3:a+=c;c=[];continue
 x,y,z=map(int,l);z+=y
 for i,j in a:c+=(f:=z>i<j>y)*[(max(i,y)-y+x,min(j,z)-y+x)];b+=[[(i,j)],[(i,y-1)]*(i<y)+[(z+1,j)]*(j>z)][f]
 a,*b=b,
print(min(a+c)[0])