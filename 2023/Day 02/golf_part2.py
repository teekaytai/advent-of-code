import re
t=0
for l in open(0):
 d={}
 for n,c in re.findall('(\d+) (.)',l):d[c]=max(d.get(c,0),int(n))
 t+=d['r']*d['g']*d['b']
print(t)