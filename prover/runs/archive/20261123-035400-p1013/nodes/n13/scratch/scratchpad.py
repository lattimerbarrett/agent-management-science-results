import networkx as nx,itertools
L=12
inds=[]
for mask in range(1<<L):
 if not mask&(mask<<1): inds.append([i for i in range(L) if mask>>i&1])
found=[]
for E in itertools.combinations(range(0,L,2),4):
 for O in itertools.combinations(range(1,L,2),4):
  S=set(E+O);H=nx.path_graph(L);H.add_node(L);H.add_edges_from((L,x) for x in S)
  ms=L
  for v in H:
   F=H.copy();F.remove_node(v)
   if not nx.is_bipartite(F):continue
   co=nx.bipartite.color(F);k=0
   for C in nx.connected_components(F):
    nums=[sum(H.has_edge(v,x) and co[x]==b for x in C) for b in [0,1]]
    k+=min(nums)
   ms=min(ms,k)
  if ms<4:continue
  forbidK4=False;forbidK33=False;forbidC3=False;forbidC4=False
  badcycles=set([12])
  for I in inds:
   J=H.copy();J.remove_nodes_from(I)
   Cs=[J.subgraph(c) for c in nx.connected_components(J)]
   if all(len(c)<=4 for c in Cs):forbidK4=True
   if all(nx.is_bipartite(c) and max([sum(b==z for b in nx.bipartite.color(c).values()) for z in [0,1]])<=3 for c in Cs):forbidK33=True
   if all(len(c)<=3 for c in Cs):forbidC3=True
   if all(nx.is_bipartite(c) and max([sum(b==z for b in nx.bipartite.color(c).values()) for z in [0,1]])<=2 for c in Cs):forbidC4=True
  if forbidK4 and forbidK33:
   found.append((tuple(sorted(S)),forbidC3,forbidC4));print('found',found[-1],flush=True)
print('count',len(found))