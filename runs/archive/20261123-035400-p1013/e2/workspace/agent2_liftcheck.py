import networkx as nx,functools,json,itertools
E=json.load(open('workspace/agent4_found.json'))
def colorable(G,r):
 p={};adj={v:set(G[v]) for v in G}
 def go():
  if len(p)==len(G):return True
  v=max((u for u in G if u not in p),key=lambda u:(len({p[w] for w in adj[u] if w in p}),len(adj[u])))
  bad={p[w] for w in adj[v] if w in p}
  for c in range(min(r,max(p.values(),default=-1)+2)):
   if c not in bad:
    p[v]=c
    if go():return True
    del p[v]
  return False
 return go()
def candidate(r):
 G=nx.Graph(E)
 for _ in range(r-3):G=nx.convert_node_labels_to_integers(nx.full_join(G,nx.empty_graph(2),rename=('a','b')))
 return G
def min_active(G,r):
 n=len(G);adj=[sum(1<<u for u in G[v]) for v in G];blocks=[[] for _ in G]
 for mask in range(1,1<<n):
  vs=[v for v in G if mask>>v&1];ds=[(adj[v]&mask).bit_count() for v in vs]
  if max(ds)<=1:
   for v in vs:blocks[v].append((mask,int(max(ds)>0)))
 @functools.lru_cache(None)
 def go(mask,left):
  if not mask:return 0 if left==0 else 100
  if not left or mask.bit_count()<left:return 100
  v=(mask&-mask).bit_length()-1
  return min((cost+go(mask^b,left-1) for b,cost in blocks[v] if b&mask==b),default=100)
 return go((1<<n)-1,r)
def verify(r):
 G=candidate(r)
 assert colorable(G,r+1) and not colorable(G,r)
 for v in G:
  R=G.copy();R.remove_node(v)
  for e in list(R.edges()):
   J=R.copy();J.remove_edge(*e)
   assert not colorable(J,r),(r,v,e)
 ma=min_active(G,r);assert ma>2
 for mask in range(1<<len(G)):
  vs=[v for v in G if mask>>v&1]
  if any(len(c)>3 for c in nx.connected_components(G.subgraph(vs))):continue
  assert not colorable(G.subgraph([v for v in G if not(mask>>v&1)]),r-1)
 print(r,'all robustness/template tests passed; minimum matching-active classes',ma,flush=True)
if __name__=='__main__':
 for r in range(3,8):verify(r)
