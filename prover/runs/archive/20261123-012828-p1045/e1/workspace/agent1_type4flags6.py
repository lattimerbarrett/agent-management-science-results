import numpy as np
import networkx as nx
from itertools import permutations,combinations
from pathlib import Path

def build():
 fn=Path('workspace/agent1_type4flags6.npz')
 if fn.exists():return np.load(fn)['M']
 gs=[g for g in nx.graph_atlas_g() if len(g)==6]
 M=np.zeros((64,16,16,len(gs)))
 rp=list(combinations(range(4),2))
 for gi,g in enumerate(gs):
  A=nx.to_numpy_array(g,dtype=int)
  for roots in permutations(range(6),4):
   typ=sum(int(A[roots[i],roots[j]])<<k for k,(i,j) in enumerate(rp))
   y,z=[x for x in range(6) if x not in roots]
   u=sum(int(A[y,roots[i]])<<i for i in range(4))
   v=sum(int(A[z,roots[i]])<<i for i in range(4))
   M[typ,u,v,gi]+=1/720
   M[typ,v,u,gi]+=1/720
 assert np.max(abs(M-M.swapaxes(1,2)))<1e-12
 assert np.allclose(M.sum(axis=(0,1,2)),1)
 np.savez_compressed(fn,M=M)
 return M
if __name__=='__main__':
 M=build();print('Built',M.shape)
 data=np.load('workspace/agent3_extremal_vectors6.npz');print('validation keys',data.files)
 for key in data.files:
  x=data[key]
  if x.shape!=(156,):continue
  ev=np.linalg.eigvalsh(np.einsum('tijk,k->tij',M,x))
  print(key,'min_eig',ev.min())
  assert ev.min()>-1e-10
