"""Six-vertex induced-density coefficients for rooted book constraints.
Graph order agrees NetworkX graph_atlas_g restricted to order 6.
For root color c and each rooted 5vertex flag F (3 unlabelled leaves),
(cap_c B0 - B1) @ induced_densities >=0 encodes
E[1_{root color c} 1_F (cap_c-common_color_c)]>=0.
"""
import networkx as nx
import numpy as np
from itertools import permutations
from functools import lru_cache

@lru_cache(None)
def canon(pats, edges):
 # pats ordered length3 root adjacency bitpairs; edge bits for 01,02,12.
 def E(i,j):
  return edges[{(0,1):0,(0,2):1,(1,2):2}[tuple(sorted((i,j)))]]
 return min(tuple(pats[i] for i in p)+tuple(E(p[i],p[j]) for i,j in [(0,1),(0,2),(1,2)]) for p in permutations(range(3)))

def build_books6():
 from itertools import product
 keys=sorted({canon(pats,edges) for pats in product(range(4),repeat=3) for edges in product(range(2),repeat=3)})
 idx={key:i for i,key in enumerate(keys)}
 graphs=[g for g in nx.graph_atlas_g() if len(g)==6]
 nf=len(keys);ng=len(graphs)
 B0=np.zeros((2*nf,ng));B1=np.zeros_like(B0)
 for gi,g in enumerate(graphs):
  E=lambda u,v:int(g.has_edge(u,v))
  for u,v in permutations(range(6),2):
   col=E(u,v);rem=[x for x in range(6) if x not in (u,v)]
   for x in rem:
    leaves=[y for y in rem if y!=x]
    pats=tuple(2*E(u,y)+E(v,y) for y in leaves)
    edges=tuple(E(leaves[i],leaves[j]) for i,j in [(0,1),(0,2),(1,2)])
    fi=col*nf+idx[canon(pats,edges)]
    B0[fi,gi]+=1/120
    if E(u,x)==col and E(v,x)==col:
     B1[fi,gi]+=1/120
 assert nf==120 and ng==156
 assert np.allclose(B0.sum(axis=0),1)
 assert np.min(B1)>=0 and np.max(B1-B0)<1e-10
 return graphs,B0,B1,keys

if __name__=='__main__':
 graphs,B0,B1,keys=build_books6()
 np.savez('workspace/agent3_books6.npz',B0=B0,B1=B1,keys=np.array(keys))
 print('Checked/saved',B0.shape,'rooted six-vertex book coefficient arrays')
