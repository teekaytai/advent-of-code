for R in zip(*open(t:=0)):c=p=len(R)+1;t+=sum((b:=s>'N')*(p:=[p,c:=c-1][s<'.']-b)for s in R)
print(t)