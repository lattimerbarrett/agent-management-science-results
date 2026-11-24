import networkx as nx
from z3 import *
def maps(G,h):
 H=nx.cycle_graph(h); s=Solver(); x=[Int('x%d'%i) for i in G]
 for a in x:s.add(a>=0,a<h)
 for u,v in G.edges:s.add(Or(*[And(x[u]==a,x[v]==b) for a,b in H.edges for a,b in [(a,b),(b,a)]]))
 return s.check()
for r in range(1,4):
 p=5*r+2;q=2*r+1
 G=nx.Graph();G.add_nodes_from(range(p))
 for i in range(p):
  for j in range(i):
   if q<=i-j<=p-q:G.add_edge(i,j)
 print(r,p,min(dict(G.degree()).values())/p,'to C5',maps(G,5),'to C7',maps(G,7))
