g=open(0).read()
q={8645}
for _ in[0]*64:q={z+d for z in q for d in(-132,1,132,-1)if'#'<g[z+d]}
print(len(q))