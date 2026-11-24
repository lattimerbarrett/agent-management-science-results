import networkx as nx,z3,json

def feasible(G,b,D):
 S=z3.Solver();A={v:z3.Bool(f'a{v}') for v in G};C={v:z3.Bool(f'c{v}') for v in G}
 S.add(z3.PbLe([(c,1) for c in C.values()],1))
 for v in G:
  S.add(z3.Implies(C[v],A[v]))
  da=[A[w] for w in G[v]];db=[z3.Not(A[w]) for w in G[v]]
  if da:
   S.add(z3.Implies(z3.And(A[v],z3.Not(C[v])),z3.PbLe([(x,1) for x in da],1)))
   S.add(z3.Implies(C[v],z3.PbLe([(x,1) for x in da],D-1)))
   S.add(z3.Implies(z3.Not(A[v]),z3.PbLe([(x,1) for x in db],1)))
 S.add(z3.PbLe([(z3.And(z3.Not(A[u]),z3.Not(A[v])),1) for u,v in G.edges()],b))
 return S.check()==z3.sat
