a=b=q=0
for l in open(0):n=int(l[-8:-3],16);p=q;q+=1j**int(l[-3])*n;a+=2*p.imag*(p-q).real;b+=n
print(int(abs(a)+b+2)//2)