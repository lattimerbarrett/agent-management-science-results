from sage.all import Graph
from itertools import product,combinations
import networkx as nx
import numpy as np
import sympy as sp
import time,pickle,os

def enumerate_seq(n,typ):
 targets=([2] if typ=='end' else [2,2])+[4]*(n-(1 if typ=='end' else 2))
 roots=1 if typ=='end' else 2
 adj=[0]*n
 seen=[set() for _ in range(n+1)]
 outputs=[];calls=0
 def dfs(done):
  nonlocal calls
  calls+=1
  remain=[i for i in range(n) if not(done>>i&1)]
  ds={i:targets[i]-adj[i].bit_count() for i in remain}
  if not nx.is_graphical(list(ds.values())):return
  parts=[]
  for role in range(2):
   for status in range(2):
    group=[i for i in range(n) if (i<roots)==(role==0) and (done>>i&1)==status]
    if group:parts.append(group)
  G=Graph(n)
  G.add_edges((i,j) for i in range(n) for j in range(i) if adj[i]>>j&1)
  key=(tuple(map(len,parts)),G.canonical_label(partition=parts).graph6_string())
  dep=done.bit_count()
  if key in seen[dep]:return
  seen[dep].add(key)
  if not remain:
   if G.is_connected():outputs.append(G.graph6_string())
   return
  special=[i for i in remain if i<roots]
  u=special[0] if special else max(remain,key=lambda i:ds[i])
  cand=[v for v in remain if v!=u and ds[v]>0]
  groups={}
  for v in cand:groups.setdefault((v<roots,adj[v],ds[v]),[]).append(v)
  groups=list(groups.values())
  for counts in product(*(range(min(len(g),ds[u])+1) for g in groups)):
   if sum(counts)!=ds[u]:continue
   ns=[v for g,c in zip(groups,counts) for v in g[:c]]
   for v in ns:adj[v]|=1<<u;adj[u]|=1<<v
   dfs(done|1<<u)
   for v in ns:adj[v]^=1<<u;adj[u]^=1<<v
 dfs(0)
 return outputs,calls,[len(s) for s in seen]

def compute(n,typ):
 fn=f'{typ}{n}.pickle'
 if os.path.exists(fn):
  gs=pickle.load(open(fn,'rb'))
 else:
  t=time.time();gs,calls,counts=enumerate_seq(n,typ)
  pickle.dump(gs,open(fn,'wb'))
  print('generated',n,typ,len(gs),calls,counts,'secs',time.time()-t,flush=True)
 best=-1;bestg=None;pair=None
 for st in gs:
  G=Graph(st);L=np.array(G.laplacian_matrix(),dtype=float)
  P=np.linalg.pinv(L)
  if typ=='end':pairs=[(0,j) for j in range(1,n)]
  else:pairs=[(0,1)]
  for u,v in pairs:
   r=P[u,u]+P[v,v]-2*P[u,v]
   if r>best+1e-8:best=r;bestg=st;pair=(u,v)
 G=Graph(bestg);u,v=pair
 L=sp.Matrix([list(row) for row in G.laplacian_matrix().rows()]);L.row_del(v);L.col_del(v)
 r=L.inv()[u-(u>v),u-(u>v)]
 print('BEST',n,typ,r,'edges',G.edges(labels=False),'pair',pair,flush=True)
 return r,bestg,pair

if __name__=='__main__':
 for n in range(6,11):
  for typ in ['end','internal']:compute(n,typ)
