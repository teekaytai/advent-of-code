for l in open(t:=0):
 *a,=map(int,l.split())
 while any(a):t+=a[0];a=[x-y for x,y in zip(a,a[1:])]
print(t)