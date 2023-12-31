g=open(0).read()
W=g.index('\n')+1
q=[(0,1)]
for z,d in q:m=lambda*D:[(z+d,d)for d in D];q+=[p for p in[m(-1,1),*[m(d)]*4,m(-W,W),m(d//-W),m(d*-W),m(d//W),m(d*W)]['-.|/'.find(g[z])*2+d*d%W]if(W*W-W>p[0]>=0and' '<g[p[0]])*~-(p in q)]
print(len({z for z,_ in q}))