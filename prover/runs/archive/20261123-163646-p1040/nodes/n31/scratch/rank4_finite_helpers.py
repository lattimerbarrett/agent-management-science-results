import time, numpy as np, pickle, os
from itertools import product
from collections import defaultdict
from scipy.sparse import coo_matrix
N=4;D=7
words=[w for d in range(1,D+1) for w in product(range(N),repeat=d)]
IX={w:j for j,w in enumerate(words)};M=len(words)
def gens():
 G={};names=[]
 for i in range(N):
  for j in range(N):
   if i==j:continue
   a=[(k+1,) for k in range(N)];b=a.copy();a[i]=(j+1,i+1,-j-1);b[i]=(-j-1,i+1,j+1)
   idx=len(names)+1;G[idx]=a;G[-idx]=b;names.append(('K',i,j))
  for j in range(N):
   for k in range(j+1,N):
    if i in (j,k):continue
    a=[(l+1,) for l in range(N)];b=a.copy();a[i]=(i+1,j+1,k+1,-j-1,-k-1);b[i]=(i+1,k+1,j+1,-k-1,-j-1)
    idx=len(names)+1;G[idx]=a;G[-idx]=b;names.append(('C',i,j,k))
 return G,names
G,names=gens()
def mul(P,Q):
 R=defaultdict(int)
 for u,c in P.items():
  for v,e in Q.items():
   if len(u)+len(v)<=D:R[u+v]+=c*e
 return {w:c%3 for w,c in R.items() if c%3}
def build(g):
 pol=[]
 for w in g:
  P={():1}
  for a in w:
   i=abs(a)-1;Q={():1,(i,):1} if a>0 else {(i,)*k:(-1)**k for k in range(D+1)}
   P=mul(P,Q)
  P.pop((),None);pol.append(P)
 cache={():{():1}};rr=[];cc=[];vv=[]
 for j,w in enumerate(words):
  P=mul(cache[w[:-1]],pol[w[-1]]);cache[w]=P
  for v,c in P.items():rr.append(IX[v]);cc.append(j);vv.append(c)
 return coo_matrix((np.array(vv,dtype=np.int16),(rr,cc)),shape=(M,M)).tocsr()
