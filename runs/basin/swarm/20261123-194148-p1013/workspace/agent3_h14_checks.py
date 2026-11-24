import networkx as nx
E=[(0,8),(0,9),(0,11),(0,13),(1,6),(1,7),(1,11),(1,13),(2,9),(3,6),(3,7),(4,10),(4,11),(4,12),(4,13),(5,7),(5,8),(5,9),(7,13),(10,13),(12,13)]
H=nx.Graph();H.add_nodes_from(range(14));H.add_edges_from(E)
ad=[sum(1<<w for w in H[u]) for u in range(14)];full=(1<<14)-1
assert not nx.is_bipartite(H) and nx.is_bipartite(H.subgraph(range(13)))
def comps(mask):
 out=[];unseen=mask
 while unseen:
  todo=unseen&-unseen;c=0
  while todo:
   bit=todo&-todo;todo^=bit;v=bit.bit_length()-1;c|=bit;unseen&=~bit;todo|=ad[v]&mask&~c
  vs=[v for v in range(14)if c>>v&1];ds=[(ad[v]&c).bit_count()for v in vs]
  out.append((len(vs),sum(ds)//2,max(ds,default=0),c))
 return out
pmin=tmin=smin=999;wp=wt=ws=None
for A in range(1<<14):
 B=full^A;ca=comps(A);cb=comps(B)
 if all(d<=1 for k,e,d,c in ca+cb):
  s=min(sum(e for k,e,d,c in ca),sum(e for k,e,d,c in cb))
  if s<smin:smin=s;ws=A
 if any(e for k,e,d,c in cb):continue
 if all(k<=3 for k,e,d,c in ca):
  t=sum(k==3 for k,e,d,c in ca)
  if t<tmin:tmin=t;wt=A
  if all(e<k for k,e,d,c in ca) and t<pmin:pmin=t;wp=A
assert (pmin,tmin,smin)==(3,3,3)
# P4 and claw decompositions with independent complements.
for A,expected in [({4,6,7,8,9,11,13},{(4,11),(4,13),(7,13)}),({0,1,2,3,4,5,13},{(0,13),(1,13),(4,13)})]:
 assert not H.subgraph(set(H)-A).number_of_edges()
 assert set(H.subgraph(A).edges())==expected
# Mixed P3+edge witness: endpoint13 complete to P3 vertices; endpoint7 anticomplete.
A={0,1,2,3,4,5,10,12};B=set(H)-A
assert set(H.subgraph(A).edges())=={(4,10),(4,12)}
assert set(H.subgraph(B).edges())=={(7,13)}
assert all(H.has_edge(13,u) and not H.has_edge(7,u)for u in [4,10,12])
print('H14 all16384partitions checked: pmin=tmin=smin=3; all decomposition/mixed witnesses checked.')
for name,m in [('P3',wp),('C3',wt),('matchingboth',ws)]:
 A={v for v in range(14)if m>>v&1};print(name,sorted(A),list(H.subgraph(A).edges()),list(H.subgraph(set(H)-A).edges()))
