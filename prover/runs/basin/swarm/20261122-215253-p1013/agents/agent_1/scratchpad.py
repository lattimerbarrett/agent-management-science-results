import pickle,networkx as nx
Gs=pickle.load(open('small_counter_candidates.pkl','rb'))
for G,vs,fs in Gs:
 n=len(G);decs=[];pairs=[]
 for mask in range(1<<n):
  U=[u for u in G if mask>>u&1];V=[u for u in G if not mask>>u&1]
  F=G.subgraph(U);B=G.subgraph(V)
  if max(dict(F.degree()).values(),default=0)<=1 and max(dict(B.degree()).values(),default=0)<=1:pairs.append((F.number_of_edges(),B.number_of_edges()))
  if B.number_of_edges()==0:
   F=F.copy();F.remove_nodes_from(list(nx.isolates(F)))
   if not any(nx.is_isomorphic(F,J) for J in decs):decs.append(F)
 print('pairs',set(pairs),'decs',[ (len(F),F.number_of_edges(),sorted(dict(F.degree()).values())) for F in decs])
 for typ in ['K3','C4','C5','C6','K4']:
  C=nx.complete_graph(int(typ[1:])) if typ.startswith('K') else nx.cycle_graph(int(typ[1:]))
  host=nx.disjoint_union_all([C]*4)
  emb=any(nx.algorithms.isomorphism.GraphMatcher(host,F).subgraph_is_monomorphic() for F in decs)
  print(typ,emb,end=';')
 print()
