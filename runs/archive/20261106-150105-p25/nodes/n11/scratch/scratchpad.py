import networkx as nx
import numpy as np
from itertools import combinations
m,k=6,2
sets=list(combinations(range(m),k))
Q=nx.Graph();Q.add_nodes_from(range(len(sets)))
Q.add_edges_from((u,v) for u,v in combinations(Q,2) if set(sets[u]).isdisjoint(sets[v]))
G=nx.Graph();classes={};label={}
for u in Q:
 x=('v',u);G.add_node(x);classes[x]=0;label[x]=set(sets[u])
for u,v in Q.edges:
 a=('a',u,v);b=('b',u,v)
 G.add_edges_from([(('v',u),a),(a,b),(b,('v',v))])
 classes[a]=1;label[a]=set(sets[u])
 classes[b]=2;label[b]=set(sets[v])
Fverts=list(G)
for c in range(3):
 for i in range(m):
  A=('A',c,i);B=('B',c)
  G.add_edge(A,B)
  for v in Fverts:
   if classes[v]==c and i in label[v]:G.add_edge(A,v)
M=nx.to_numpy_array(G,dtype=np.int64)
print('core vertices / edges:',Q.number_of_nodes(),Q.number_of_edges())
print('extension vertices / edges:',G.number_of_nodes(),G.number_of_edges())
print('closed walks of length 3:',np.trace(np.linalg.matrix_power(M,3)))
print('closed walks of length 5:',np.trace(np.linalg.matrix_power(M,5)))
# Give each A vertex weight T and each B vertex weight k*T.
# Every F vertex retains weight 1. This describes an integer blow-up.
for T in [100,10000]:
 weights={v:(T if v[0]=='A' else k*T if v[0]=='B' else 1) for v in G}
 n=sum(weights.values());delta=min(sum(weights[w] for w in G[v]) for v in G)
 print('blowup n,delta,ratio:',n,delta,delta/n)
print('general asymptotic density: k/(3*(m+k)); tends to 1/9 for m/k -> 2')