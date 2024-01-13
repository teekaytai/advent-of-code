m=open(0).read()
W=m.find('\n')+1
t=i=0
while i<len(m):
 j,n=i,'0'
 while'/'<m[j]<':':n+=m[j];j+=1
 i,t=j+1,t+int(n)*any({*m[r+i-1:r+j+1]}&{*'#$%&*+-/=@'}for r in(-W,0,W))
print(t)