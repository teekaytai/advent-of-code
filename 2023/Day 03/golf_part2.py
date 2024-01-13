N=len(m:=open(i:=0).read())
W=m.find('\n')+1
G=[[]]*N
while i<N:
 j,n=i,'0'
 while'/'<m[j]<':':n+=m[j];j+=1
 for r in(-W,0,W):
  k=r+i-1
  for c in m[k:r+j+1]:G[k]=G[k]+[int(n)]*(j>i)*('*'==c);k+=1
 i=j+1
print(sum(g[0]*g[1]for g in G if len(g)==2))