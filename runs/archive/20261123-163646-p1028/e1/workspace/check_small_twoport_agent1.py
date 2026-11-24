import networkx as nx, itertools, json, sympy as s
from pathlib import Path

def graphs_degree(degs):
 n=len(degs); adj=[set() for _ in range(n)]
 def rec(i,ds):
  if i==n:
   G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from((u,v) for u in range(n) for v in adj[u] if u<v);yield G;return
  cand=[j for j in range(i+1,n) if ds[j]>0]
  if ds[i]<0 or ds[i]>len(cand):return
  for ns in itertools.combinations(cand,ds[i]):
   dd=ds.copy();dd[i]=0
   for j in ns:dd[j]-=1
   if not nx.is_graphical(dd[i+1:],method='eg'):continue
   for j in ns:adj[i].add(j);adj[j].add(i)
   yield from rec(i+1,dd)
   for j in ns:adj[i].remove(j);adj[j].remove(i)
 yield from rec(0,list(degs))

out={}
for n in (6,7):
 best=s.Rational(0);count=0;bestedges=[]
 for G in graphs_degree([2,2]+[4]*(n-2)):
  if not nx.is_biconnected(G):continue
  count+=1
  L=s.zeros(n-1)
  for u in range(1,n):
   L[u-1,u-1]=G.degree(u)
   for v in G[u]:
    if v:L[u-1,v-1]=-1
  R=L.inv()[0,0]
  if R>best:best=R;bestedges=list(G.edges())
 out[n]={'count':count,'Rmax':str(best),'defect':str(s.Rational(n-1,4)-best),'edges':bestedges}
 print(n,out[n],flush=True)
Path('workspace/agent1_small_twoport.json').write_text(json.dumps(out,indent=2))
