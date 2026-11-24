import networkx as nx,sys,itertools,json,time
from pathlib import Path
sys.path.insert(0,'workspace');from agent2_hole_cegar import minholes
H=nx.Graph();H.add_nodes_from(range(15));H.add_edges_from([(0,1),(6,7)])
H.add_edges_from((0,j) for j in [2,3]);H.add_edges_from((1,j) for j in [4,5]);H.add_edges_from((6,j) for j in [8,9,10]);H.add_edges_from((7,j) for j in [11,12,13]);H.add_edges_from((14,j) for j in list(range(2,6))+list(range(8,14)))
assert nx.is_bipartite(nx.subgraph(H,range(14)))
assert [v for v in H if nx.is_bipartite(H.subgraph(set(H)-{v}))]==[14]
red={0,1,6,7,14};assert sorted(H.subgraph(red).edges())==[(0,1),(6,7)];assert H.subgraph(set(H)-red).number_of_edges()==0
T=[nx.Graph()]+[nx.star_graph(d) for d in range(1,5)]+[nx.complete_graph(3)]
names=['empty','edge','P3','claw','star4','tri'];out=[];st=time.time()
for i,A in enumerate(T):
 for j in range(i,len(T)):
  B=T[j];I=A.number_of_edges()+B.number_of_edges()
  if I<6:continue
  res=minholes(H,A,B,cap=I-6,limit=500)
  row={'A':names[i],'B':names[j],'I':I,'cap':I-6,'result':res};out.append(row);print(row,flush=True)
res1=minholes(H,T[4],T[0]);print('ALT',res1)
Path('workspace/agent2_H15_odd_a0_checks.json').write_text(json.dumps({'H':list(H.edges()),'checks':out,'alternative':res1,'seconds':time.time()-st},indent=2))
Path('workspace/agent2_H15_odd_a0_checks.py').write_text(Path(__file__).read_text())
