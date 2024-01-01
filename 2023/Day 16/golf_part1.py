g=open(0).read()
W=g.find('\n')+1
q=[(0,1)]
for z,d in q:m=lambda*D:[(z+d,d)for d in D];q+=[p for p in[m(-1,1),*[m(d)]*4,m(-W,W),m(d//-W),m(d*-W),m(d//W),m(d*W)]['-.|/'.find(g[z])*2+d*d%W]if-1<p[0]<W*W*(W-p[0]%W>1)*-~-(p in q)-W]
print(len({z for z,_ in q}))