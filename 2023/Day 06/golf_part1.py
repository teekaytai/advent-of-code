p=1
for t,d in zip(*[map(int,l.split()[1:])for l in open(0)]):p*=sum(d<i*(t-i)for i in range(t))
print(p)