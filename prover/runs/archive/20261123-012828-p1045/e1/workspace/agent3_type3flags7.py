import numpy as np
import networkx as nx
from itertools import combinations,permutations
from pathlib import Path

def build():
 fn=Path('workspace/agent3_type3flags7.npz')
 if fn.exists():return np.load(fn)['M']
 G=[g for g in nx.graph_atlas_g() if len(g)==7]
 patterns=[(i,j,e) for i in range(8) for j in range(i,8) for e in range(2)]
 idx={p:i for i,p in enumerate(patterns)}
 reps=[0,1,3,7];ri={t:i for i,t in enumerate(reps)}
 M=np.zeros((4,72,72,1044))
 for gi,g in enumerate(G):
  A=nx.to_numpy_array(g,dtype=int)
  for u,v,w in permutations(range(7),3):
   typ=4*A[u,v]+2*A[u,w]+A[v,w]
   if typ not in ri:continue
   rem=[x for x in range(7) if x not in (u,v,w)]
   pats={x:4*A[u,x]+2*A[v,x]+A[w,x] for x in rem}
   def flag(x,y):return idx[min(pats[x],pats[y]),max(pats[x],pats[y]),A[x,y]]
   for yz in combinations(rem,2):
    st=[x for x in rem if x not in yz]
    M[ri[typ],flag(*yz),flag(*st),gi]+=1/1260
 assert np.max(abs(M-M.swapaxes(1,2)))<1e-12
 np.savez_compressed(fn,M=M)
 return M
if __name__=='__main__':
 M=build();print('built',M.shape)
 f=np.load('workspace/agent3_random7.npz')['density']
 for mat in M:
  ev=np.linalg.eigvalsh(np.einsum('ijk,k->ij',mat,f))
  assert ev.min()>-1e-12 and ev[-2]<1e-12
 print('validated homogeneous moments PSD rank1')
