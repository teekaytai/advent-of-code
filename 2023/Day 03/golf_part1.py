N=len(m:=[*open(0)])
t=r=0
for l in m:
 i=0
 while i<N:
  j,n=i,'0'
  while j<N and'/'<l[j]<':':n+=l[j];j+=1
  i,t=j+1,t+int(n)*any(N>R>=0and{*m[R][max(i-1,0):j+1]}&{*'#$%&*+-/=@'}for R in(r-1,r,r+1))
 r+=1
print(t)