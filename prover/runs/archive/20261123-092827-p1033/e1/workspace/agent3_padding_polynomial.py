from itertools import combinations,product
from math import comb

def build(t):
 X=[];n=0
 for i in range(1,t+1):X.append(set(range(n,n+i)));n+=i
 P=[[frozenset(X[i]|set(a)) for a in product(*[tuple(X[j]) for j in range(i+1,t)])] for i in range(t)]
 return n,X,P

def countcovers(V,F,s):
 return sum(all(set(c)&e for e in F) for c in combinations(V,s))
for t in range(2,5):
 n,X,P=build(t)
 coeff=[0]*(t+1)
 for mask in range(1<<t):
  I=[i for i in range(t) if mask>>i&1];s=len(I)
  c=countcovers(range(n),[e for i in I for e in P[i]],s)
  coeff[t-s]+=c
 for L in range(3):
  Y=[set(range(n+i*L,n+(i+1)*L)) for i in range(t)]
  Fs=[e|frozenset(Y[i]) for i in range(t) for e in P[i]]
  actual=countcovers(range(n+t*L),Fs,t)
  predicted=sum(c*L**j for j,c in enumerate(coeff))
  assert actual==predicted,(t,L,actual,predicted)
 assert coeff[t]==1 and coeff[t-1]==sum(map(len,X))
 print(t,coeff,'all L=0,1,2 verified')
