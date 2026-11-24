import networkx as nx, random, functools, json
from fractions import Fraction
random.seed(4027)
D=nx.complete_bipartite_graph(2,3)
atlas=[g for g in nx.graph_atlas_g() if len(g)>=2 and len(g)<=6 and nx.is_connected(g) and Fraction(g.number_of_edges(),len(g))>Fraction(6,5)]
bad=[]
for g in sorted(atlas,key=lambda g:(g.number_of_edges(),len(g))):
 if not any(nx.isomorphism.GraphMatcher(g,f).subgraph_is_monomorphic() for f in bad):bad.append(g)
bad.append(nx.star_graph(4))
print('bad',[(len(g),g.number_of_edges()) for g in bad],flush=True)
@functools.lru_cache(None)
def fits(key,di):
 F=nx.from_graph6_bytes(key); Q=([D]+bad)[di]
 return len(F)<=len(Q) and nx.isomorphism.GraphMatcher(Q,F).subgraph_is_monomorphic()
def residuals(H):
 n=len(H); adj=[sum(1<<j for j in H[i]) for i in range(n)]; out=[]
 for mask in range(1<<n):
  unseen=mask; color0=0; color1=0; ok=True
  while unseen and ok:
   todo=unseen&-unseen; color0|=todo; unseen^=todo
   while todo and ok:
    u=(todo&-todo).bit_length()-1;todo&=todo-1
    own=color0 if color0>>u&1 else color1
    if adj[u]&own:ok=False;break
    nei=adj[u]&unseen;todo|=nei;unseen^=nei
    if color0>>u&1:color1|=nei
    else:color0|=nei
  if not ok:continue
  rem=((1<<n)-1)^mask; cs=[]
  while rem:
   root=rem&-rem; comp=root; todo=root; rem^=root
   while todo:
    u=(todo&-todo).bit_length()-1;todo&=todo-1
    nei=adj[u]&rem;todo|=nei;comp|=nei;rem^=nei
   vs=[i for i in range(n) if comp>>i&1]
   F=nx.convert_node_labels_to_integers(H.subgraph(vs));cs.append(nx.to_graph6_bytes(F,header=False).strip())
  out.append(cs)
 return out
def emb(res,di):return any(all(fits(k,di) for k in cs) for cs in res)
found=0
for it in range(10000):
 nt=random.choice([6,7,8,9]); T=random.choice(list(nx.generators.nonisomorphic_trees(nt)))
 H=nx.convert_node_labels_to_integers(T,first_label=2); H.add_edge(0,1)
 for i in range(2,nt+2):
  for a in [0,1]:
   if random.random()<.6:H.add_edge(a,i)
 if not any(len(c)>=4 for c in nx.find_cliques(H)):continue
 res=residuals(H)
 if emb(res,0):continue
 if all(emb(res,di+1) for di in range(len(bad))):
  print('FOUND',it,list(H.edges()),flush=True);found+=1
  with open('workspace/agent3_candidate.json','w') as f:json.dump({'edges':list(H.edges())},f)
  break
 if it%1000==0:print(it,'cache',fits.cache_info(),flush=True)
print('done',found,flush=True)
