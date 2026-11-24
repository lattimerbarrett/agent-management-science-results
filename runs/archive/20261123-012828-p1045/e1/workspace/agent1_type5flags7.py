import networkx as nx
import numpy as np
from itertools import combinations,permutations
from pathlib import Path

def build():
 fn=Path('workspace/agent1_type5flags7.npz')
 if fn.exists():return np.load(fn)['M']
 atlas=nx.graph_atlas_g();reps=[g for g in atlas if len(g)==5];gs=[g for g in atlas if len(g)==7]
 ps=list(combinations(range(5),2));mapping={}
 for ti,g in enumerate(reps):
  A=nx.to_numpy_array(g,dtype=int)
  for pm in permutations(range(5)):
   code=sum(int(A[pm[i],pm[j]])<<k for k,(i,j) in enumerate(ps))
   inv=tuple(pm.index(j) for j in range(5))
   if code in mapping:assert mapping[code][0]==ti;mapping[code][1].append(inv)
   else:mapping[code]=(ti,[inv])
 assert len(mapping)==1024
 M=np.zeros((34,32,32,1044))
 for gi,g in enumerate(gs):
  A=nx.to_numpy_array(g,dtype=int)
  for roots in combinations(range(7),5):
   code=sum(int(A[roots[i],roots[j]])<<k for k,(i,j) in enumerate(ps))
   typ,orders=mapping[code];y,z=[x for x in range(7) if x not in roots]
   for order in orders:
    r=[roots[i] for i in order]
    u=sum(int(A[y,r[i]])<<i for i in range(5));v=sum(int(A[z,r[i]])<<i for i in range(5))
    M[typ,u,v,gi]+=1/5040;M[typ,v,u,gi]+=1/5040
 assert np.max(abs(M-M.swapaxes(1,2)))<1e-12
 np.savez_compressed(fn,M=M)
 return M
if __name__=='__main__':
 M=build();D=np.load('workspace/agent1_extremal_vectors7.npz')
 for name in ['random','tripartite']:
  H=np.einsum('tijk,k->tij',M,D[name]);ev=np.linalg.eigvalsh(H)
  print(name,'min',ev.min(),'maxrank',(ev>1e-12).sum(axis=1).max(),flush=True)
  assert ev.min()>-1e-12
 print('Built',M.shape)
