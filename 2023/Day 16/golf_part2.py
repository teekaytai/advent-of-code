N=len(g:=open(0).read())
W=g.find('\n')+1
def f(s):
 q=[s]
 for z,d in q:m=lambda*D:[(z+d,d)for d in D];q+=[p for p in[m(-1,1),*[m(d)]*4,m(-W,W),m(d//-W),m(d*-W),m(d//W),m(d*W)]['-.|/'.find(g[z])*2+d*d%W]if-1<p[0]<N*(W-p[0]%W>1)*-~-(p in q)]
 return len({z for z,_ in q})
print(max(max(map(f,zip([N-i-2,W*i,i,W*i+W-2],[-W,1,W,-1])))for i in range(W-1)))