*g,=open(0).read()
G=g.index
W=G('\n')+1
f=lambda z:{z+d for d in[[-W,W],[1,-1],[-W,1],[-W,-1],[W,-1],[1,W],[]]['|-LJ7F'.find(g[z])]}
p=s=G(S:='S')
q,_=[s+d for d in(-W,1,W,-1)if-1<s+d<len(g)and s in f(s+d)]
i=1
while q!=s:p,[q]=q,f(q)-{p};i+=1
print(i//2)