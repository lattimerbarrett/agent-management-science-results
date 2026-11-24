import networkx as nx,z3

def packing_embedding(G,F):
 """Exact embedding in complete bipartite with arbitrary copies of F in A.
 Returns set A, independent complement B, or None. All solvers exact.
 Lazy component cuts are valid since every induced component that fails
 subgraph-monomorphism into F is itself a forbidden non-induced subgraph.
 """
 vs=list(G);a={u:z3.Bool('aa'+str(u))for u in vs};D=max(dict(F.degree()).values(),default=0)
 s=z3.Solver();s.add([z3.Or(a[u],a[v])for u,v in G.edges])
 s.add([z3.Implies(a[u],z3.PbLe([(a[w],1)for w in G[u]],D))for u in vs if G.degree(u)>D])
 while s.check()==z3.sat:
  m=s.model();A=[u for u in vs if z3.is_true(m.eval(a[u]))];bad=[]
  for C in nx.connected_components(G.subgraph(A)):
   if len(C)>len(F)or not nx.algorithms.isomorphism.GraphMatcher(F,G.subgraph(C)).subgraph_is_monomorphic():bad.append(C)
  if not bad:return set(A)
  for C in bad:s.add(z3.Or([z3.Not(a[u])for u in C]))
 return None

def check_certificate(G,F,A):
 if A is None:return False
 B=set(G)-set(A)
 return not G.subgraph(B).number_of_edges() and all(len(C)<=len(F) and nx.algorithms.isomorphism.GraphMatcher(F,G.subgraph(C)).subgraph_is_monomorphic()for C in nx.connected_components(G.subgraph(A)))
