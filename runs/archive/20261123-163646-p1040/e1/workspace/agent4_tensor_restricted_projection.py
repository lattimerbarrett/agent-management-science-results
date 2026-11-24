from itertools import product
from pathlib import Path
import numpy as np,json,time

def lyndon(w):return all(w<w[k:]+w[:k] for k in range(1,len(w)))
def pivots(maxd):
 M=sum(3**d for d in range(5,maxd+1));P=[]
 for d in range(5,maxd+1):
  S=set();power=1
  while d%power==0:
   n=d//power
   for u in product(range(3),repeat=n):
    if lyndon(u):S.add(u*power)
   power*=3
  offset=sum(3**k for k in range(5,d))
  ids=[]
  for w in sorted(S):
   k=0
   for a in w:k=3*k+a
   ids.append(offset+k)
  print('degree',d,'restrictedLyndonpivots',len(ids))
  P+=ids
 return np.array([i*M+j for i in range(3) for j in P],dtype=np.int32)
P=pivots(9);np.save('workspace/agent4_tensor_d9_restricted_pivots.npy',P)
print('D9projectionlength',len(P))
# Independently verify compression on prior exact D8 gamma4 basis.
from sage.all import load,GF,matrix
p=Path('workspace/agent3_gamma4_tensor_basis.sobj')
if p.exists():
 t=time.time();B=load(str(p));P8=pivots(8);C=B.matrix_from_columns(list(map(int,P8)))
 print('D8basis',B.dimensions(),'compressed',C.dimensions(),'exactrank',C.rank(),'seconds',time.time()-t)
 assert C.rank()==B.nrows()==3338
