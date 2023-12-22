*I,=open(0)
R=range(N:=len(I))
f=lambda G,s=0:[(s:=s+1+999999*(l.count('.')==N))for l in G]
g=[(f(I)[r],f(zip(*I))[c])for r in R for c in R if'.'>I[r][c]]
print(sum(abs(y-Y)+abs(x-X)for y,x in g for Y,X in g)//2)