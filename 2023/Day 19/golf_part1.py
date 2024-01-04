S=str.split
A,B=S(open(t:=0).read(),'\n\n')
W=dict(S(a[:-1],'{')for a in S(A))
for b in S(B):
 v='in'
 while'R'<v:
  *w,v=S(W[v],',')
  for x in w[::-1]:c,u=S(x,':');v=[v,u][eval(f'(p:=dict({b[1:-1]}))["{c[0]}"]'+c[1:])]
 t+=(v<'R')*sum(p.values())
print(t)