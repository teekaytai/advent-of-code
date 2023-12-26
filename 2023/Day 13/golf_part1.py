f=lambda S:sum(c for c in range(len(S))if(s:=S[c-(k:=min(c,len(S)-c)):c+k])==s[::-1])
print(sum(100*f(g:=p.split())+f([*zip(*g)])for p in open(0).read().split('\n\n')))