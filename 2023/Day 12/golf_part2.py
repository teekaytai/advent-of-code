from functools import*
for l in open(t:=0):S,a=l.split();g=a.split(',')*5;N=len(S:='?'.join([S]*5));f=cache(lambda i,j:B%2*-~-('#'in S[i:])if(B:=(j==len(g))+2*(i>=N))else(S[i]>'#')*f(i+1,j)+-~-(N<(k:=i+int(g[j]))or'.'in S[i:k]or'#'==S[k:k+1])*f(k+1,j+1));t+=f(0,0)
print(t)