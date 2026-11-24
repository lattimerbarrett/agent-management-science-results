import json,networkx as nx,z3,sys
sys.path.insert(0,'workspace');from agent3_packing_host import packing_embedding
H=nx.Graph(json.load(open('workspace/agent3_allcycle_p4_counter.json'))['edges'])
def newgraph(L):
 G=H.copy();G.remove_edge(15,3)
 aa=[15,len(G),len(G)+1];bb=[3,len(G)+2,len(G)+3]
 G.add_edges_from((a,b)for a in aa for b in bb if (a,b)!=(15,3))
 prev,current=1,15
 for j in range(L):
  p,b=len(G),len(G)+1;G.add_edges_from([(prev,b),(b,p),(current,p)]);prev,current=current,p
 return nx.convert_node_labels_to_integers(G)
def pred(G):
 R=[z3.Bool('r'+str(i))for i in G];s=z3.Solver();s.add(R[0])
 for u,v in G.edges():s.add(z3.Or(R[u],R[v]))
 for u in G:s.add(z3.PbLe([(z3.And(R[u],R[v]),1)for v in G[u]],2))
 for it in range(10000):
  if s.check()==z3.unsat:return None
  m=s.model();A={u for u in G if z3.is_true(m.eval(R[u]))};cs=nx.cycle_basis(G.subgraph(A))
  if not cs:return A
  for C in cs:s.add(z3.Or([z3.Not(R[u])for u in C]))
for L in range(1,8):
 G=newgraph(L);A=pred(G);print('L',L,'vREDpath?',A)
 vals=[]
 for k in range(3,12):
  A=packing_embedding(G,nx.path_graph(k))
  if A is not None:vals=[k,A];break
 print('pathmin',vals,'claw?',packing_embedding(G,nx.star_graph(3)) is not None,'C3?',packing_embedding(G,nx.cycle_graph(3)) is not None,'C4?',packing_embedding(G,nx.cycle_graph(4)) is not None,flush=True)
 print('cycle hosts',[(j,packing_embedding(G,nx.cycle_graph(j)) is not None)for j in range(3,L+5)],flush=True)
from pathlib import Path
Path('workspace/agent3_path_family_checks.py').write_text(Path(__file__).read_text())
