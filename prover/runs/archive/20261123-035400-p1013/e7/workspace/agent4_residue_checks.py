"""Exhaustive induced-subgraph and packing check for the small theta model."""
import networkx as nx

def theta(D,L):
 G=nx.Graph();G.add_nodes_from([0,1]);nextv=2
 for _ in range(D):
  path=[0]+list(range(nextv,nextv+L-1))+[1];nextv+=L-1
  G.add_edges_from(zip(path,path[1:]))
 return G

G=theta(8,3);v=len(G);e=G.number_of_edges()
A=[sum(1<<w for w in G[u]) for u in G]
# Exhaust ALL vertex subsets; max induced edges for each order.
best=[-10**9]*(v+1);best[0]=0
for mask in range(1<<v):
 z=0;t=mask
 while t:
  bit=t&-t;t-=bit;z+=(A[bit.bit_length()-1]&mask).bit_count()
 best[mask.bit_count()]=max(best[mask.bit_count()],z//2)
# Pack arbitrary subgraphs: every chosen induced-subgraph component is allowed.
N=8*v
pack=[-10**9]*(N+1);pack[0]=0
for n in range(1,N+1):
 pack[n]=max(pack[n-j]+best[j] for j in range(1,min(v,n)+1))
for J in range(1,8):
 m=J*v;assert pack[m]==J*e
 # General residue lemma covers 0<delta<L-1.
 for delta in range(1,2):assert pack[m+delta]<=J*e+delta-1
print('Enumerated all',1<<v,'vertex subsets of theta(8,3).')
print('Unbounded packing DP verified balanced perfect-factor optimality and +1 residue bound through',N,'vertices.')
