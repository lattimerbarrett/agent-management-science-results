import networkx as nx
import numpy as np
from itertools import combinations
from scipy.sparse import csr_matrix
m,r,L=5,2,1
sets=list(map(frozenset,combinations(range(m),r)))
Q=nx.Graph();Q.add_nodes_from(range(len(sets)))
Q.add_edges_from((u,v) for u,v in combinations(Q.nodes,2) if sets[u].isdisjoint(sets[v]))
F=nx.Graph();F.add_nodes_from(Q);C=[list(Q),[],[]];phi={u:sets[u] for u in Q}
for u,v in Q.edges:
 a=('a',u,v);b=('b',u,v)
 C[1].append(a);C[2].append(b)
 F.add_edges_from([(u,a),(a,b),(b,v)])
 phi[a]=sets[v];phi[b]=sets[u]
violations=[]
for u in F:
 reach={u}
 for _ in range(3):reach={w for v in reach for w in F[v]}
 for v in reach:
  if not phi[u].isdisjoint(phi[v]):violations.append((u,v))
print('Failure of three-walk label disjointness:',len(violations))
G=F.copy()
for j in range(3):
 B=[('B',j,k) for k in range(r*L)]
 for i in range(m):
  A=[('A',j,i,k) for k in range(L)]
  G.add_edges_from((a,b) for a in A for b in B)
  G.add_edges_from((v,a) for v in C[j] if i in phi[v] for a in A)
A=csr_matrix(nx.to_scipy_sparse_array(G,dtype=np.int64)); A2=A@A;A3=A2@A
print('Triangle closed walks:',A.multiply(A2).sum())
print('Length-five closed walks:',A2.multiply(A3).sum())
print('F vertices:',len(F),'G vertices:',len(G),'minimum degree:',min(dict(G.degree()).values()))
print('Asymptotic min-degree proportion for fixed m,r:',r/(3*(m+r)))
print('As m/r tends to 2, proportion tends to',1/9)
