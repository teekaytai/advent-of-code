g=open(p:=0).read()
G=g.find
W=G('\n')+1
s=G('S')
f=lambda z:{z+d for d in[[-W,W],[1,-1],[-W,1],[-W,-1],[W,-1],[1,W],[]]['|-LJ7F'.find(g[s+z])]}
q,_=[d for d in(-W,1,W,-1)if-1<s+d<len(g)and 0in f(d)]
i=1
while q:p,[q]=q,f(q)-{p};i+=1
print(i//2)