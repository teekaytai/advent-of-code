t,d=[int(''.join(l.split()[1:]))for l in open(0)]
print(sum(d<i*(t-i)for i in range(t)))