S=sorted
def f(p):
 t=0;h=p[0];a,b,c,d,e=S(S(H:=h.replace(J:='J',([J]+S({*h}-{J},key=h.count))[-1])),key=H.count)
 for x in h:t=t*14+'23456789TQKA'.find(x)
 return((a==b)+2*(b==c)+3*(c==d)+(d==e))*1e6+t
i=0
print(sum((i:=i+1)*int(b)for _,b in S(map(str.split,open(0)),key=f)))