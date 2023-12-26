f=lambda S:sum(c*(sum(x!=y for i in range(min(c,len(S)-c))for x,y in zip(S[c-i-1],S[c+i]))==1)for c in range(len(S)))
print(sum(100*f(g:=p.split())+f([*zip(*g)])for p in open(0).read().split('\n\n')))