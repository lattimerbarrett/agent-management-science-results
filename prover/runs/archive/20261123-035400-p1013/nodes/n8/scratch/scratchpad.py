import networkx as nx
import mpmath as mp
from fractions import Fraction
H=nx.Graph()
H.add_edges_from([(0,i) for i in range(1,5)]+[(1,2),(2,3),(3,4),(4,1)]+[(1,5),(5,6),(6,1),(3,7),(7,8),(8,3)])
print('H vertex count:',len(H),'edge count:',H.number_of_edges())
print('H-v bipartite:',{v:nx.is_bipartite(nx.subgraph_view(H,filter_node=lambda w,v=v:w!=v)) for v in H})
print('P5-induced edges:',sorted(H.subgraph([5,1,0,3,7]).edges()))
print('Complement independent:',H.subgraph([2,4,6,8]).number_of_edges()==0)
mp.mp.dps=40
A=mp.nsum(lambda j:1/mp.factorial(j)**2,[0,mp.inf])
B=mp.nsum(lambda j:1/(mp.factorial(j)*mp.factorial(j+1)),[0,mp.inf])
D=mp.nsum(lambda j:mp.mpf(2)**(2*j+1)/(mp.factorial(j)*mp.factorial(j+1)),[0,mp.inf])
print('Matching cycle limit:',D)
print('Hub cycle limit:',2*(A+B))
for r in range(2,7):
 print('r=',r,'matching coefficient=',Fraction(1,2*r),'universal coefficient=',Fraction(1,r))
