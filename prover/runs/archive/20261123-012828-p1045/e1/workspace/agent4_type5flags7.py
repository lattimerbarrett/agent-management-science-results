import numpy as np,networkx as nx
from itertools import combinations,permutations
from pathlib import Path

def build():
 path=Path('workspace/agent4_type5flags7.npz')
 if path.exists():return np.load(path)['M']
 types=[g for g in nx.graph_atlas_g() if len(g)==5];graphs=[g for g in nx.graph_atlas_g() if len(g)==7]
 es=list(combinations(range(5),2));ei={e:i for i,e in enumerate(es)};maps=[[] for _ in range(1024)];typs=np.full(1024,-1)
 for t,g in enumerate(types):
  for pm in permutations(range(5)):
   mask=sum(1<<ei[tuple(sorted((pm[u],pm[v])))] for u,v in g.edges())
   assert typs[mask] in (-1,t)
   typs[mask]=t;maps[mask].append(pm)
 assert np.all(typs>=0)
 M=np.zeros((34,32,32,1044))
 for gi,g in enumerate(graphs):
  adj=nx.to_numpy_array(g,dtype=np.int8)
  for roots in combinations(range(7),5):
   mask=sum(int(adj[roots[u],roots[v]])<<j for j,(u,v) in enumerate(es));t=typs[mask];ys=[i for i in range(7) if i not in roots];y,z=ys;norm=1/(42*len(maps[mask]))
   for pm in maps[mask]:
    a=sum(int(adj[roots[pm[j]],y])<<j for j in range(5));b=sum(int(adj[roots[pm[j]],z])<<j for j in range(5))
    M[t,a,b,gi]+=norm;M[t,b,a,gi]+=norm
 assert np.max(abs(M.sum(axis=(0,1,2))-1))<1e-12
 assert np.max(abs(M-M.transpose(0,2,1,3)))<1e-12
 np.savez_compressed(path,M=M)
 return M
if __name__=='__main__':
 M=build();d=np.load('workspace/agent4_extremal_vectors7.npz')
 for key in ['random','tripartite']:
  worst=0;ranks=[]
  for mat in M:
   H=np.einsum('ijk,k->ij',mat,d[key]);ev=np.linalg.eigvalsh(H);worst=min(worst,min(ev));ranks.append(sum(ev>1e-12))
  print(key,'worst',worst,'ranks',ranks)
