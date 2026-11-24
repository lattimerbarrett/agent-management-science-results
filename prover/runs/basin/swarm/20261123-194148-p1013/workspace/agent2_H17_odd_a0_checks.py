import networkx as nx,sys,itertools,json,time
from pathlib import Path
sys.path.insert(0,'workspace');from agent2_hole_cegar import minholes
H=nx.Graph();H.add_nodes_from(range(17));H.add_edges_from([(0,1),(8,9)])
H.add_edges_from((0,j) for j in [2,3,4]);H.add_edges_from((1,j) for j in [5,6,7]);H.add_edges_from((8,j) for j in [10,11,12]);H.add_edges_from((9,j) for j in [13,14,15]);H.add_edges_from((16,j) for j in list(range(2,8))+list(range(10,16)))
assert nx.is_bipartite(nx.subgraph(H,range(16)))
assert [v for v in H if nx.is_bipartite(H.subgraph(set(H)-{v}))]==[16]
red={0,1,8,9,16};assert sorted(H.subgraph(red).edges())==[(0,1),(8,9)];assert H.subgraph(set(H)-red).number_of_edges()==0
T=[nx.Graph()]+[nx.star_graph(d) for d in range(1,6)]+[nx.complete_graph(3)]
names=['empty','edge','P3','claw','star4','star5','tri'];out=[];st=time.time()
for i,A in enumerate(T):
 for j in range(i,len(T)):
  B=T[j];I=A.number_of_edges()+B.number_of_edges()
  if I<6:continue
  res=minholes(H,A,B,cap=I-6,limit=500)
  row={'A':names[i],'B':names[j],'I':I,'cap':I-6,'result':res};out.append(row);print(row,flush=True)
res1=minholes(H,T[5],T[0]);print('ALT',res1)
Path('workspace/agent2_H17_odd_a0_checks.json').write_text(json.dumps({'H':list(H.edges()),'checks':out,'alternative':res1,'seconds':time.time()-st},indent=2))
assert len(out)==13
for row in out:
 if row['A']==row['B']=='tri':assert row['result']['status']=='ok' and row['result']['holes']==0
 else:assert row['result']['status'] in ('unsat','impossible'),row
assert res1['status']=='ok' and res1['holes']==0
print('ALL H17 FINITE EMBEDDING ASSERTIONS PASSED')
