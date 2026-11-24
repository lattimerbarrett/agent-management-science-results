"""Independent exact checks of the H8 obstruction, not a claim about ex()."""
import networkx as nx
from math import factorial
from fractions import Fraction
from collections import defaultdict
from agent3_cycles import brute_cycles
H=nx.from_graph6_bytes(b'GE`cFs')
P={1:{(0,0):1,(1,1):1},2:{(0,0):1,(1,1):2,(2,2):1,(2,1):2},3:{(0,0):1,(1,1):3,(2,2):3,(2,1):4,(3,3):1,(3,2):4,(3,1):2}}
def count(a,b):
 p={(0,0):1}
 for z in [3]*(a//3)+([a%3] if a%3 else []):
  q=defaultdict(int)
  for (v,k),c in p.items():
   for (w,l),d in P[z].items():q[v+w,k+l]+=c*d
  p=q
 twice=sum(c*factorial(k-1)*factorial(b)//factorial(b-k) for (v,k),c in p.items() if 1<=k<=b and v+k>=3)
 assert twice%2==0
 return twice//2

def host(a,b):
 g=nx.complete_bipartite_graph(a,b)
 for j in range(a//3):g.add_edges_from([(3*j,3*j+1),(3*j+1,3*j+2)])
 if a%3==2:g.add_edge(a-2,a-1)
 return g

def verify():
 assert nx.is_bipartite(H.subgraph(set(H)-{7}))
 assert all(H.has_edge(u,v) for u,v in [(0,3),(3,7),(0,7)])
 # The three embedding certificates into a complete-cross host: specify special vertices.
 expected=[({0,1,2,7},nx.star_graph(3)),({0,1,5,7},nx.path_graph(4)),({0,3,5,7},nx.disjoint_union(nx.cycle_graph(3),nx.empty_graph(1)))]
 for A,F in expected:
  assert H.subgraph(set(H)-A).number_of_edges()==0
  assert nx.is_isomorphic(H.subgraph(A),F)
 # Embedding with one edge in each complete-cross part.
 A={0,5,7};B=set(H)-A
 assert list(H.subgraph(A).edges())==[(0,7)]
 assert list(H.subgraph(B).edges())==[(1,3)]
 # H cannot fit complete-cross P3packing-onepart: enumerate ALL choices of special vertices.
 for S in range(1<<8):
  A={v for v in H if S>>v&1}
  if H.subgraph(set(H)-A).number_of_edges():continue
  F=H.subgraph(A)
  assert any(len(C)>3 or F.subgraph(C).number_of_edges()>2 for C in nx.connected_components(F))
 # Independent DFS checks, including omitted-vertex terms.
 for a,b in [(3,3),(4,2),(6,4),(6,5),(7,4)]:assert count(a,b)==brute_cycles(host(a,b))
 # Rational certificates of the limiting strict cycle inequality.
 K=20;z=Fraction(7,3)
 A=sum((z**t/factorial(t)**2 for t in range(K+1)),Fraction())
 nextA=z**(K+1)/factorial(K+1)**2
 upperA=A+nextA/(1-z/Fraction((K+2)**2))
 D=sum((z**(t+2)/(factorial(t)*factorial(t+2)) for t in range(K+1)),Fraction())
 assert D>upperA
 # Exact finite comparison (no floating point in the assertion).
 assert count(25,23)>count(24,24)
 return float(A),float(D),float(D/A),float(Fraction(count(25,23),count(24,24)))
if __name__=='__main__':print('All H8 finite and rational certificates passed:',verify())
