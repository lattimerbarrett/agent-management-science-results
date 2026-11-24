from itertools import combinations
from exact_decomp_a4 import subfaces,facets,kd,complex_from_facets
from agent2_nearcone import nearcone_order

def vertices(C):
 return frozenset().union(*C)

def completion(C,k,A):
 """Returns missing facet order proving bound d-2 for d>=3,k>=1."""
 q=len(next(iter(facets(C))));d=q-1
 assert k>=1 and d>=2
 assert len(A)==max(0,d-2) and not (vertices(C)&set(A))
 V=vertices(C)
 if d==2:
  X=C;order=[]
  while True:
   candidate=None
   for ff in combinations(sorted(V),3):
    F=frozenset(ff)
    if F in X:continue
    if sum(frozenset(e) in X for e in combinations(ff,2))>=2:
     candidate=F;break
   if candidate is None:break
   order.append(candidate);X=X|subfaces(candidate)
  assert all(frozenset(f) in X for f in combinations(V,3))
  return order
 a=A[0];B=A[1:]
 order=[r|{a} for r in nearcone_order(C,k)]
 G=frozenset(f for f in C if len(f)<=d)
 order.extend(F|{a} for F in completion(G,k,B))
 W=V|set(B)
 order.extend(frozenset(f) for f in combinations(sorted(W),q) if frozenset(f) not in C)
 assert len(order)==len(set(order))
 return order

def verify(C,k,A):
 from a3_fastkd import kd as fastkd
 def exact(C,k):
  return fastkd(tuple(sorted(sum(1<<v for v in f) for f in facets(C))),k)
 X=C;order=completion(C,k,A)
 assert exact(X,k)
 for F in order:
  assert F not in X
  X=X|subfaces(F)
  assert exact(X,k),('non-kd intermediate',facets(C),k,A,F)
 W=vertices(C)|set(A);q=len(next(iter(facets(C))))
 assert facets(X)==frozenset(frozenset(f) for f in combinations(W,q))
 return len(order)

if __name__=='__main__':
 import random,json
 random.seed(223)
 results=[]
 for n,d,trials in [(6,3,50),(6,4,63)]:
  Fs=[frozenset(f) for f in combinations(range(n),d+1)]
  masks=range(1,1<<len(Fs)) if trials==(1<<len(Fs))-1 else random.sample(range(1,1<<len(Fs)),trials)
  pairs=steps=0
  for mask in masks:
   C=complex_from_facets([F for j,F in enumerate(Fs) if mask>>j&1])
   for k in range(1,d+1):
    if kd(C,k):
     steps+=verify(C,k,list(range(n,n+d-2)));pairs+=1
  results.append(dict(n=n,d=d,checked_pairs=pairs,checked_additions=steps))
  print(results[-1],flush=True)
 json.dump(results,open('workspace/agent2_upper_dminus2_checks.json','w'))
