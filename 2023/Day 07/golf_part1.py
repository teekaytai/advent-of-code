S=sorted
def f(p):
 t=0;a,b,c,d,e=S(S(h:=p[0]),key=h.count)
 for x in h:t=t*14+'3456789TJQKA'.find(x)
 return((a==b)+2*(b==c)+3*(c==d)+(d==e))*1e6+t
i=0
print(sum((i:=i+1)*int(b)for _,b in S(map(str.split,open(0)),key=f)))