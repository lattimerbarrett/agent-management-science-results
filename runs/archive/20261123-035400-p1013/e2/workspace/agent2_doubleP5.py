import networkx as nx,functools,itertools

def colorable(G,r):
 nodes=list(G); adj={v:set(G[v]) for v in G};p={}
 def go():
  if len(p)==len(nodes):return True
  v=max((u for u in nodes if u not in p),key=lambda u:(len({p[w] for w in adj[u] if w in p}),len(adj[u])))
  bad={p[w] for w in adj[v] if w in p}
  for c in range(min(r,max(p.values(),default=-1)+2)):
   if c not in bad:
    p[v]=c
    if go():return True
    del p[v]
  return False
 return go()
def cand(r):
 G=nx.path_graph(5)
 for J in [nx.path_graph(5)]+[nx.empty_graph(2) for _ in range(r-3)]:G=nx.convert_node_labels_to_integers(nx.full_join(G,J,rename=('a','b')))
 return G
for r in range(3,7):
 G=cand(r);n=len(G); robust=True
 for v in G:
  R=G.copy();R.remove_node(v)
  for e in R.edges():
   J=R.copy();J.remove_edge(*e)
   if colorable(J,r):print('FAIL',r,v,e);robust=False;break
  if not robust:break
 print(r,n,'robust',robust)
def min_active(G,r):
 n=len(G);full=(1<<n)-1;blocks={i:[] for i in range(n)}
 for k in range(1,5):
  for vs in itertools.combinations(range(n),k):
   g=G.subgraph(vs)
   if max(dict(g.degree()).values())<=1:
    mask=sum(1<<v for v in vs);cost=int(g.number_of_edges()>0)
    for v in vs:blocks[v].append((mask,cost))
 @functools.lru_cache(None)
 def go(mask,left):
  if not mask:return 0 if left==0 else 100
  if not left or mask.bit_count()<left:return 100
  v=(mask&-mask).bit_length()-1
  return min((cost+go(mask^b,left-1) for b,cost in blocks[v] if b&mask==b),default=100)
 return go(full,r)
for r in range(3,7):print('active',r,min_active(cand(r),r))
# self-copy disabled: ("# self-copy disabled: ", "# self-copy disabled: "))
