import networkx as nx,itertools
import mpmath as mp
mp.mp.dps=40
H=nx.Graph();H.add_edges_from([(0,3),(0,4),(0,6),(0,7),(1,3),(1,5),(1,7),(2,5),(2,7),(3,7),(4,7),(6,7)])
print('H minus 7 bipartite:',nx.is_bipartite(nx.subgraph(H,[0,1,2,3,4,5,6])))
allowed=[]
for bits in range(256):
 A=[v for v in range(8) if bits>>v&1];B=[v for v in range(8) if not bits>>v&1]
 F=H.subgraph(A)
 if H.subgraph(B).number_of_edges()==0 and all(len(C)<=3 and nx.is_tree(F.subgraph(C)) for C in nx.connected_components(F)):
  allowed.append(A)
print('Forbidden-graph partitions into P3 components and independent complement:',allowed)
for n in range(1,1001):
 f=max(a*(n-a)+(2*a)//3 for a in range(n+1))
 g=n*n//4+(n+n%2)//3
 assert f==g,(n,f,g)
print('Extremal arithmetic identity checked for n <= 1000')
z=mp.mpf(7)/3
A=mp.besseli(0,2*mp.sqrt(z));D=z*mp.besseli(2,2*mp.sqrt(z))
print('P3 construction cycle limits A,D,D-A:',A,D,D-A)
