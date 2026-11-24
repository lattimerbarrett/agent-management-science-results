from itertools import combinations
from exact_decomp_a4 import subfaces,facets,complex_from_facets
from agent2_nearcone import witness,nearcone_order

def vertices(C):return frozenset().union(*C)

def completion(C,W=None):
 """Facetwise vertex-decomposable completion on a prescribed ground set W."""
 W=frozenset(vertices(C) if W is None else W)
 X=C;order=[];q=len(next(iter(facets(C))))
 if q==0:return []
 for w in sorted(W-vertices(X)):
  F=next(iter(facets(X)));H=frozenset(sorted(F)[:-1]);G=H|{w}
  order.append(G);X=X|subfaces(G)
 if len(facets(X))==1:return order
 if q==1:return order
 s,D,L=witness(X,0);v=next(iter(s))
 first=completion(D,W-{v});order.extend(first)
 second=completion(L,W-{v});order.extend(s|H for H in second)
 return order

def verify(C,W=None):
 from a3_fastkd import kd
 def exact(X):return kd(tuple(sorted(sum(1<<v for v in f) for f in facets(X))),0)
 X=C;W=vertices(C) if W is None else frozenset(W);q=len(next(iter(facets(C))))
 order=completion(C,W)
 assert exact(X)
 for F in order:
  assert F not in X
  X=X|subfaces(F);assert exact(X)
 assert facets(X)==frozenset(frozenset(F) for F in combinations(W,q))
 return len(order)
