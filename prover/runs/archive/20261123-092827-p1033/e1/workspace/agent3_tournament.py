from itertools import product,combinations
def construction(t):
 X=[];v=0
 for i in range(t):
  X.append(frozenset(range(v,v+i+1)));v+=i+1
 P=[[X[i]|frozenset(a) for a in product(*[tuple(X[j]) for j in range(i+1,t)])] for i in range(t)]
 return set(range(v)),X,P
for t in range(2,6):
 V,X,P=construction(t);F=sum(P,[])
 assert all(len(e)==t for e in F)
 assert len(F)==len(set(F))
 assert all(e&f for e in F for f in F)
 assert all(X[i]<=e for i in range(t) for e in P[i])
 assert all(not(X[i]&X[j]) for i in range(t) for j in range(i))
 for C in combinations(V,t-1):
  assert any(not(set(C)&e) for e in F)
 assert sum(t-len(x) for x in X)==t*(t-1)//2
 print(t,len(V),len(F),t*(t-1)//2)
