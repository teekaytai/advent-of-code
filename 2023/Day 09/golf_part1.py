for l in open(t:=0):
 *a,=map(int,l.split())
 while a:t+=a[-1];a=[y-x for x,y in zip(a,a[1:])]
print(t)