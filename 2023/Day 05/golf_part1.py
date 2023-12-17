s,b,*L=map(str.split,open(0))
*a,=map(int,s[1:])
c=[]
for l in L:
 if len(l)<3:a+=c;c=[];continue
 x,y,z=map(int,l)
 for w in a:c+=(f:=y<=w<y+z)*[w-y+x];b+=-~-f*[w]
 a,*b=b,
print(min(a+c))