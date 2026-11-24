from itertools import combinations
from collections import defaultdict

def powerset(S):
 L=list(S)
 for q in range(len(L)+1):
  for A in combinations(L,q):yield frozenset(A)
def tau_gt(H,r):
 if any(not E for E in H):return True
 U=set().union(*H)
 return all(any(not E&set(C) for E in H) for q in range(r+1) for C in combinations(U,q))
def kernelize(F,X,r):
 fibers=defaultdict(set)
 for E in F:fibers[frozenset(E-X)].add(frozenset(E&X))
 result=set();report=[]
 for G,T in fibers.items():
  candidates=set().union(*(set(powerset(E)) for E in T))
  flowers=[]
  for A in sorted(candidates,key=lambda a:(len(a),tuple(sorted(a)))):
   if any(B<=A for B in flowers):continue
   link={E-A for E in T if A<=E}
   if link and tau_gt(link,r):flowers.append(A)
  assert all(any(A<=E for A in flowers) for E in T)
  for A in flowers:result.add(G|A)
  report.append((sorted(G),[sorted(E) for E in T],[sorted(A) for A in flowers]))
 assert all(any(K<=E for E in F) for K in result)
 assert all(A&B for A in result for B in result)
 return result,report
# Cyclic rank-one t=3 original example.
cores=[set(range(2*i,2*i+2)) for i in range(3)]
F=[frozenset(cores[i]|{v}) for i in range(3) for v in cores[(i+1)%3]]
Ri={2}; H=[E for E in F if not E&Ri and not cores[0]<=E]
K,report=kernelize(H,cores[0],1)
print('old',list(map(sorted,H)));print('new',list(map(sorted,K)));print('fibers',report)
# A synthetic robust trace fiber: traces are 3 disjoint singletons, r=2.
H=[frozenset({10,11,a}) for a in [0,1,2]]+[frozenset({10,12,3})]
K,report=kernelize(H,{0,1,2,3},2)
print('robust old/new',list(map(sorted,H)),list(map(sorted,K)));print(report)
import pathlib
pathlib.Path('workspace/agent4_block_flower.py').write_text(pathlib.Path('scratchpad.py').read_text())
