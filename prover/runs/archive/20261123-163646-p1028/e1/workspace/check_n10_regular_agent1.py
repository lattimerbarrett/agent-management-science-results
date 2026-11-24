import sys,time,json
from pathlib import Path
import networkx as nx,sympy as s
sys.path.insert(0,'workspace')
from enumerate_local4 import graphs_degseq
out=[]
for n,d in [(10,3),(10,4)]:
 best=s.Integer(0);count=0;witness=None;t=time.time()
 for edges in graphs_degseq([d]*n):
  G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from(edges)
  if not nx.is_connected(G):continue
  count+=1
  L=s.eye(n)*d
  for a,b in edges:L[a,b]=L[b,a]=-1
  Z=L[1:,1:].inv()
  r=max([Z[i,i] for i in range(n-1)]+[Z[i,i]+Z[j,j]-2*Z[i,j] for i in range(n-1) for j in range(i)])
  if d*n*r>best:best=d*n*r;witness=edges
 res={'n':n,'d':d,'count':count,'tau_max':str(best),'edges':witness};out.append(res)
 print(res,'time',time.time()-t,flush=True)
assert out[0]['tau_max']=='165/2'
assert s.Rational(out[1]['tau_max'])<=s.Rational(165,2)
Path('workspace/exact_n10_regular_agent1.json').write_text(json.dumps(out,indent=2))
