import networkx as nx
from z3 import Solver,Int,Or,And,Not,Sum,If,sat
H8=nx.Graph();H8.add_nodes_from(range(8));H8.add_edges_from([(0,3),(0,4),(0,6),(0,7),(1,3),(1,5),(1,7),(2,5),(2,7),(3,7),(4,7),(6,7)])
H9=nx.Graph();H9.add_nodes_from(range(9));H9.add_edges_from([(0,i) for i in range(1,5)]+[(1,2),(2,3),(3,4),(4,1),(1,5),(5,6),(6,1),(3,7),(7,8),(8,3)])
def join_parts(H,sizes):
 G=H.copy();old=list(G)
 for size in sizes:
  new=list(range(len(G),len(G)+size));G.add_nodes_from(new)
  G.add_edges_from((u,v) for u in old for v in new);old+=new
 return G
def test(G,r,one_edge=False):
 s=Solver();c=[Int('c'+str(i)) for i in G]
 for x in c:s.add(x>=0,x<r)
 if one_edge:
  s.add(Sum([If(c[u]==c[v],1,0) for u,v in G.edges()])<=1)
 else:
  for u,v in G.edges():s.add(Or(c[u]!=c[v],And(c[u]==0,c[v]==0)))
  for v in G:
   neigh=list(G[v])
   s.add(Sum([If(And(c[v]==0,c[u]==0),1,0) for u in neigh])<=1)
 return s.check()==sat
for name,H in [('H8',H8),('H9',H9)]:
 for sizes in [[],[1],[2],[1,1],[1,2],[2,2]]:
  G=join_parts(H,sizes);r=2+len(sizes)
  print(name,'new part sizes',sizes,'r=',r,'embeds in one-matching template:',test(G,r),'has color-critical edge:',test(G,r,True),flush=True)
