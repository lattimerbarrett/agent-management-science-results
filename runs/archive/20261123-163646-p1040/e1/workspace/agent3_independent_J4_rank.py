"""Exact rational image-rank check by ALL9^4 associative derivation brackets.
No Lyndon bases, image-HNF recursion, or finite-field rank assumptions.
"""
from itertools import combinations,product
from collections import defaultdict
from sage.all import matrix,QQ

def plus(A,B,sgn=1):
 C=A.copy()
 for w,c in B.items():C[w]=C.get(w,0)+sgn*c
 return {w:c for w,c in C.items() if c}
def apply(D,P):
 C=defaultdict(int)
 for w,c in P.items():
  for pos,j in enumerate(w):
   for v,e in D[j].items():C[w[:pos]+v+w[pos+1:]]+=c*e
 return {w:c for w,c in C.items() if c}
def bracket(D,E):return tuple(plus(apply(D,E[i]),apply(E,D[i]),-1) for i in range(3))
G=[];weights=[]
for i in range(3):
 for j,k in combinations(range(3),2):
  D=[{} for _ in range(3)];D[i]={(j,k):1,(k,j):-1};G.append(tuple(D))
  weights.append(tuple(int(a==j)+int(a==k)-int(a==i) for a in range(3)))
levels=[(D,w) for D,w in zip(G,weights)]
for c in range(2,5):
 levels=[(bracket(D,E),tuple(a+b for a,b in zip(w,v))) for D,w in levels for E,v in zip(G,weights)]
 groups=defaultdict(list)
 for D,w in levels:
  if any(D):groups[w].append(D)
 total=0
 for wt,Ds in groups.items():
  keys=sorted(set((i,w) for D in Ds for i,P in enumerate(D) for w in P))
  A=matrix(QQ,[[D[i].get(w,0) for i,w in keys] for D in Ds]);total+=A.rank()
 print('ALL associative simple brackets degree',c,'count',len(levels),'EXACT QQ image rank',total,flush=True)
 assert total=={2:18,3:43,4:120}[c]
