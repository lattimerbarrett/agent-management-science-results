import numpy as np
import networkx as nx
from itertools import combinations,permutations
from pathlib import Path

def build():
 path=Path('workspace/agent4_books7.npz')
 if path.exists():
  d=np.load(path);return d['B0'],d['B1'],d['patterns']
 es=list(combinations(range(4),2));codes=np.arange(1<<14,dtype=np.int32);canon=codes.copy()
 for pm in permutations(range(4)):
  inds=list(pm)+[4+i for i in pm]+[8+es.index(tuple(sorted((pm[i],pm[j])))) for i,j in es]
  enc=np.zeros(len(codes),dtype=np.int32)
  for i,j in enumerate(inds):enc|=((codes>>j)&1)<<i
  canon=np.minimum(canon,enc)
 pats=np.unique(canon);idx=np.searchsorted(pats,canon);m=len(pats)
 print('patterns',m,flush=True)
 graphs=[g for g in nx.graph_atlas_g() if len(g)==7]
 B0=np.zeros((2*m,len(graphs)));B1=B0.copy()
 for gi,g in enumerate(graphs):
  adj=nx.to_numpy_array(g,dtype=np.int32)
  for u,v in permutations(range(7),2):
   col=adj[u,v];rem=[i for i in range(7) if i not in (u,v)]
   for x in rem:
    ys=[i for i in rem if i!=x]
    ar=[adj[u,y] for y in ys]+[adj[v,y] for y in ys]+[adj[ys[i],ys[j]] for i,j in es]
    cd=sum(t<<j for j,t in enumerate(ar));row=m*col+idx[cd]
    B0[row,gi]+=1/210
    if adj[u,x]==col and adj[v,x]==col:B1[row,gi]+=1/210
  if gi%200==0:print('graph',gi,flush=True)
 assert np.max(abs(B0.sum(axis=0)-1))<1e-12
 np.savez_compressed(path,B0=B0,B1=B1,patterns=pats)
 return B0,B1,pats
if __name__=='__main__':build()
