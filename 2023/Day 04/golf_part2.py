c=[1]*999
for l in open(i:=0):
 for j in range(len(a:=l.split())-len({*a})):c[i+j+1]+=c[i]
 i+=1
print(sum(c[:i]))