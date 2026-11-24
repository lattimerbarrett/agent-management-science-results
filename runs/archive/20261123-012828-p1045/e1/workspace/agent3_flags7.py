import numpy as np
import networkx as nx
from itertools import permutations,combinations,product
from functools import lru_cache

@lru_cache(None)
def canon_root4(bits):
 # root-neighbor bits 0,1,2 and leaf-pair bits 01,02,12
 adj=bits[:3];le=bits[3:]
 def E(i,j):return le[{(0,1):0,(0,2):1,(1,2):2}[tuple(sorted((i,j)))]]
 return min(tuple(adj[i] for i in p)+tuple(E(p[i],p[j]) for i,j in [(0,1),(0,2),(1,2)]) for p in permutations(range(3)))

def build7():
 graphs7=[g for g in nx.graph_atlas_g() if len(g)==7]
 graphs6=[g for g in nx.graph_atlas_g() if len(g)==6]
 keys=sorted({canon_root4(bits) for bits in product(range(2),repeat=6)})
 assert len(keys)==20
 ki={k:i for i,k in enumerate(keys)}
 M=np.zeros((20,20,len(graphs7)))
 for gi,g in enumerate(graphs7):
  E=lambda u,v:int(g.has_edge(u,v))
  def flag(root,leaves):
   a=tuple(E(root,i) for i in leaves)
   b=tuple(E(leaves[i],leaves[j]) for i,j in [(0,1),(0,2),(1,2)])
   return ki[canon_root4(a+b)]
  for root in range(7):
   rem=[x for x in range(7) if x!=root]
   for leaves in combinations(rem,3):
    other=[x for x in rem if x not in leaves]
    M[flag(root,leaves),flag(root,other),gi]+=1/140
 assert np.max(abs(M-M.swapaxes(0,1)))<1e-10
 assert np.max(abs(M.sum(axis=(0,1))-1))<1e-10
 # canonical labelled six-graph table, via all relabellings of atlas reps
 pairs=list(combinations(range(6),2));pairpos={p:i for i,p in enumerate(pairs)}
 table={}
 for gi,g in enumerate(graphs6):
  for perm in permutations(range(6)):
   mask=sum(1<<pairpos[tuple(sorted((perm[u],perm[v])))] for u,v in g.edges())
   table[mask]=gi
 assert len(table)==2**15
 L=np.zeros((len(graphs6),len(graphs7)))
 for gi,g in enumerate(graphs7):
  for drop in range(7):
   keep=[x for x in range(7) if x!=drop]
   mask=sum(1<<i for i,(u,v) in enumerate(pairs) if g.has_edge(keep[u],keep[v]))
   L[table[mask],gi]+=1/7
 assert np.max(abs(L.sum(axis=0)-1))<1e-10
 return graphs7,M,L,keys

if __name__=='__main__':
 graphs,M,L,keys=build7()
 np.savez_compressed('workspace/agent3_flags7.npz',M=M,L6=L,keys=keys)
 print('saved20x20 root4-flag matrix on',len(graphs),'seven-vertex graphs and6vertex lift')
