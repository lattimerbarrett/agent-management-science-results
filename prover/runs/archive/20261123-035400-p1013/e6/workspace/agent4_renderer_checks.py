"""Checks for the proposed projection-rigid forbidden-graph renderer.
This computes local payload/color identities and spectral data, NOT the huge graph.
The universal projectivity claim needs the Hoffman equality proof in Slack #273.
"""
import networkx as nx,itertools,json,math,z3,os,shutil
r=3;k=11;D=k;h=r*D+1
payload=[]
def add(name,G,mono=None):
 G=nx.convert_node_labels_to_integers(G)
 if nx.is_bipartite(G):
  p=nx.bipartite.color(G)
 else:
  p=dict(enumerate([i%2 for i in range(len(G))]));p[len(G)-1]=2
 assert all(p[a]!=p[b] for a,b in G.edges())
 if mono is None:mono={u:0 for u in G}
 assert all(mono[a]==mono[b] for a,b in G.edges())
 payload.append(dict(name=name,n=len(G),edges=list(G.edges()),p=[p[u] for u in G],mono=[mono[u] for u in G]))
add('star_K1_'+str(k),nx.star_graph(k))
add('P'+str(k+1)+'_plus_P'+str(k),nx.disjoint_union(nx.path_graph(k+1),nx.path_graph(k)))
F=nx.Graph([(0,1),(0,2),(0,3),(3,4)]);add('fork5',F)
for ell in range(3,2*k+1):add('C'+str(ell),nx.cycle_graph(ell))
add('two_edges_in_two_parts',nx.Graph([(0,1),(2,3)]),{0:0,1:0,2:1,3:1})
d=1+len(payload)
for i,P in enumerate(payload,start=1):
 P['labels']=[[P['mono'][u] if j==i else P['p'][u] for j in range(d)] for u in range(P['n'])]
 for j in range(d):
  mono_edges=[(a,b) for a,b in P['edges'] if P['labels'][a][j]==P['labels'][b][j]]
  assert mono_edges==(P['edges'] if j==i else [])
assert all(len(P['edges']) for P in payload)
Ncells=[[a]+[0]*(d-1) for a in range(r)]
assert {v[0] for v in Ncells}==set(range(r))
assert all({v[j] for v in Ncells}=={0} for j in range(1,d))
assert h>r*D
# Every full-product proper r-coloring is a projection: verify exact eigenvalue data.
eigs=[(-1)**j*(r-1)**(d-j) for j in range(d+1)]
assert min(eigs)==eigs[1] and eigs.count(eigs[1])==1
assert (-eigs[1])*r**d//(eigs[0]-eigs[1])==r**(d-1)
# Actually SAT-check no nonprojection proper 3-colorings in the first three nontrivial dimensions.
for dd in [2,3,4]:
 V=list(itertools.product(range(3),repeat=dd));cs=[z3.Int('c'+str(i)) for i in range(len(V))]
 so=z3.Solver();so.add(*[z3.And(c>=0,c<3) for c in cs])
 for a,v in enumerate(V):
  for b,w in enumerate(V[:a]):
   if all(x!=y for x,y in zip(v,w)):so.add(cs[a]!=cs[b])
 for j in range(dd):
  for perm in itertools.permutations(range(3)):so.add(z3.Or(*[cs[a]!=perm[v[j]] for a,v in enumerate(V)]))
 assert so.check()==z3.unsat
 print('SAT projectivity passed d=',dd)
result={'r':r,'k':k,'D':D,'h':h,'d':d,'core_vertices':h*r**d,'total_vertices':h*r**d+sum(P['n'] for P in payload)+1,'payload':payload,'root_neighbor_cells':Ncells}
with open('workspace/agent4_renderer_description.json','w') as f:json.dump(result,f)
print('All payload coloring/root/spectral checks passed:',len(payload),'payloads;',d,'coordinates;',result['total_vertices'],'vertices.')
if os.path.basename(__file__)=='scratchpad.py':shutil.copyfile(__file__,'workspace/agent4_renderer_checks.py')
