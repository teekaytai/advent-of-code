S=str.split
A,_=S(open(0).read(),'\n\n')
W=dict(S(a[:-1],'{')for a in S(A))
t=[0]
def f(v,p):
 if'S'>v:
  z=v<'R'
  for l,r in p.values():z*=r-l
  t[0]+=z;return
 *w,V=S(W[v],',')
 for x in w:y,u=S(x,':');c,o,*_=y;n=int(y[2:]);R=n,*p[c],n+1;b='<'<o;f(u,p|{c:(R[2*b+1],R[2*b])});p[c]=R[b::2]
 f(V,p)
f('in',{c:(1,4001)for c in'xmas'})
print(*t)