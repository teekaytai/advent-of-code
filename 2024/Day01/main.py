from collections import Counter
A,B = zip(*([int(x) for x in l.split()] for l in open(0).readlines()))
A=sorted(A)
B=sorted(B)
print(sum(abs(y-x) for x,y in zip(A,B)))
C = Counter(B)
print(sum(C[x]*x for x in A))
