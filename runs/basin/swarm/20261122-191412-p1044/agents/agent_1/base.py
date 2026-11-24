import networkx as nx, numpy as np, pickle, os, time
from sage.all import Matrix, GF
P=32003

def generators(T,c,p=P):
 n=len(T);m=n-1;N=1<<m
 out=[]
 for v in T:
  inc=[(i,1 if v==a else -1) for i,(a,b) in enumerate(T.edges()) if v==a or v==b]
  g=np.zeros(N,dtype=np.int64)
  for mask in range(1,1<<len(inc)):
   k=mask.bit_count()
   if k>=len(c) or not c[k]:continue
   ix=0;val=int(c[k])
   for j,(e,s) in enumerate(inc):
    if mask>>j&1:ix|=1<<e;val*=s
   g[ix]=val%p
  out.append(g)
 return out

def hilb(T,c,p=P):
 m=len(T)-1;N=1<<m;gs=generators(T,c,p)
 # c[k] equals k! coefficient
 pairs=[]
 ar=np.arange(N)
 for g in gs:
  pp=[]
  for mask in np.flatnonzero(g):
   src=ar[(ar&mask)==0];pp.append((src,src|mask,int(g[mask])))
  pairs.append(pp)
 B=np.zeros((1,N),dtype=np.int64);B[0,0]=1
 dims=[1]
 while True:
  rows=[B]
  for pp in pairs:
   z=np.zeros_like(B)
   for src,dst,a in pp:z[:,dst]=(z[:,dst]+a*B[:,src])%p
   rows.append(z)
  A=Matrix(GF(p),np.concatenate(rows));A.echelonize();r=A.rank()
  if r==len(B):break
  dims.append(r-len(B));B=np.array(A[:r].list(),dtype=np.int64).reshape(r,N)
  if r==N:break
 return tuple(dims)

def trees():
 ts=[nx.empty_graph(1)]
 for n in range(2,11):ts.extend(nx.nonisomorphic_trees(n))
 return ts
