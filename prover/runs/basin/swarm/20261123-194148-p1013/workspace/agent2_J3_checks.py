import networkx as nx,z3,json,time
from pathlib import Path
W=nx.wheel_graph(5)
Gem=nx.Graph();Gem.add_nodes_from(range(5));Gem.add_edges_from([(0,i) for i in range(1,5)]+[(1,2),(2,3),(3,4)])
F=nx.disjoint_union(W,Gem);J=nx.Graph(F);J.add_node(10);J.add_edges_from((10,i) for i in range(10))
def embeds(G,s,sel):
 n=3*s;xs=[z3.Int('x'+str(i)) for i in G.nodes];sol=z3.Solver();sol.set('timeout',120000)
 sol.add(z3.Distinct(xs));sol.add(*[z3.And(x>=0,x<n) for x in xs])
 for u,v in G.edges:
  cross=xs[u]/s!=xs[v]/s
  pairs=[z3.And(xs[u]/s==p,xs[v]/s==p,xs[u]/2==xs[v]/2) for p in sel]
  sol.add(z3.Or(cross,*pairs))
 ans=sol.check()
 return str(ans),([sol.model()[x].as_long() for x in xs] if ans==z3.sat else None)
results={}
for sel in [[0],[0,1],[0,1,2]]:
 st=time.time();r=embeds(J,6,sel);results[str(sel)]=r;print(sel,r,time.time()-st,flush=True)
assert results['[0, 1]'][0]=='unsat' and results['[0, 1, 2]'][0]=='sat'
Path('workspace/agent2_J3_checks.json').write_text(json.dumps({'edges':list(J.edges),'results':results},indent=2))
