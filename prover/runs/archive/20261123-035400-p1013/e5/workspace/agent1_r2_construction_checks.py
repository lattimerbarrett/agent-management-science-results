import networkx as nx
from pathlib import Path
import json

L=13
H=nx.Graph()
v=('v',)
H.add_node(v)
for i in range(4):
 a,b=('a',i),('b',i)
 H.add_edges_from([(v,a),(v,b),(a,b)])
for i,j in [(0,1),(1,2)]:
 for side in ['a','b']:
  for q in range(L):
   w=('w',side,i,j,q)
   H.add_edges_from([((side,i),w),(w,(side,j))])
assert H.number_of_nodes()==61 and H.number_of_edges()==116
# Forced star-4 and matching-4 colorings: internal edges only.
cs={v:0};cm={v:1};proper={v:2}
for i in range(4):
 cs['a',i]=0;cs['b',i]=1
 cm['a',i]=cm['b',i]=0
 proper['a',i]=0;proper['b',i]=1
for w in H:
 if w[0]=='w':
  cs[w]=1 if w[1]=='a' else 0
  cm[w]=1
  proper[w]=1 if w[1]=='a' else 0
assert all(proper[a]!=proper[b] for a,b in H.edges)
Es=[(a,b) for a,b in H.edges if cs[a]==cs[b]]
Em=[(a,b) for a,b in H.edges if cm[a]==cm[b]]
assert len(Es)==len(Em)==4
assert set(Es)==set((v,('a',i)) for i in range(4))
assert max(dict(nx.Graph(Em).degree()).values())==1
# Q: subdivide one edge of K_3,3.
Q=nx.complete_bipartite_graph(3,3)
Q.remove_edge(0,3);Q.add_edges_from([(0,6),(6,3)])
assert Q.number_of_nodes()==7 and Q.number_of_edges()==10
assert max(dict(Q.degree()).values())==3
assert len(nx.max_weight_matching(Q,maxcardinality=True))==3
checks={'H_vertices':61,'H_edges':116,'L':13,'star_internal_edges':len(Es),'matching_internal_edges':len(Em),'Q_edges':10,'Q_maxdegree':3,'Q_matching':3,
'cross_deletion_final_bound':[7+b-(b+2)//3 for b in range(8)]}
assert max(checks['cross_deletion_final_bound'])<=11
print(json.dumps(checks,indent=2))
Path('workspace/agent1_r2_construction_checks.json').write_text(json.dumps(checks,indent=2))
Path('workspace/agent1_r2_construction_checks.py').write_text(Path(__file__).read_text())
