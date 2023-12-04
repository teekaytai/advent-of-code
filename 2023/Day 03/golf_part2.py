N=len(m:=[*open(0)])
G=[[]for _ in[0]*N*N]
t=r=0
for l in m:
 i=0
 while i<N:
  j,n=i,'0'
  while j<N and'/'<l[j]<':':n+=l[j];j+=1
  for R in(r-1,r,r+1):
   for C in range(i-1,j+1):
    if(j>i)*(N>R>=0<=C<N)and'*'==m[R][C]:G[R*N+C]+=[int(n)]
  i=j+1
 r+=1
print(sum(g[0]*g[1]for g in G if len(g)==2))