*g,=map(str.strip,open(0))
h={}
i=4e9
while i:
 i%=h.get(G:=str(g),9e9)-i;h[G]=i;i-=1;g=[[*C[::-1]]for C in zip(*g)];t=0;r=len(g)+1
 for R in g:
  p=c=0;r-=1
  for s in R[::-1]:
   p=[p,c:=c-1][s<'.']
   if'N'<s:t+=r;p-=1;R[c],R[p]='.O'
print(t)