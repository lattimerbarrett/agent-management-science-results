import networkx as nx
for H in nx.graph_atlas_g():
 n=len(H)
 if n<3 or nx.is_bipartite(H):continue
 decomp=[]
 for b in range(1<<n):
  S=[i for i in range(n) if b>>i&1]
  if H.subgraph(S).number_of_edges():continue
  F=H.subgraph([i for i in range(n) if i not in S]);F=F.subgraph([i for i,d in F.degree() if d])
  decomp.append(F)
 if any(max(dict(F.degree()).values(),default=0)<=1 for F in decomp):continue
 if not any(nx.is_forest(F) and max(dict(F.degree()).values())==len(F)-1 for F in decomp):continue
 # if matching not forbidden but copies C4 forbidden and P3 not forbidden
 if any(len(F)<=4 and nx.algorithms.isomorphism.GraphMatcher(nx.cycle_graph(4),F).subgraph_is_monomorphic() for F in decomp):
  if not any(len(F)==3 and sorted(dict(F.degree()).values())==[1,1,2] for F in decomp):
   print('candidate',list(H.edges()),[list(F.edges()) for F in decomp]);break
else:print('none')