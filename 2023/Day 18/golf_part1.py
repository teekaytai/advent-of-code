a=b=q=0
for l in open(0):n=int(l[2:4]);p=q;q+=1j**(ord(l[0])%15)*n;a+=2*p.imag*(p-q).real;b+=n
print(int(abs(a)+b+2)//2)