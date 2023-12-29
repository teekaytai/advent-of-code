*g,=open(i:=0).read()
G=g.index
W=G('\n')+1
f=lambda z:{z+d for d in[[-W,W],[1,-1],[-W,1],[-W,-1],[W,-1],[1,W],[]]['|-LJ7F'.find(g[z])]}
p=s=G(S:='S')
q,_=[s+d for d in(-W,1,W,-1)if-1<s+d<len(g)and s in f(s+d)]
h=lambda:p%W*q//W-q%W*p//W
A=h()
while q!=s:p,[q]=q,f(q)-{p};A+=h();i+=1
print(abs(A//2)-i//2)