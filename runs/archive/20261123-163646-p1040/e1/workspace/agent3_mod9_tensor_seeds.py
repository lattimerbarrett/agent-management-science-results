import sys,time
import numpy as np
from itertools import product
from agent3_magnus import K,C,auto_commutator

def expand(w,d=8,p=9):
 starts=[(3**k-1)//2 for k in range(d+2)]
 A=np.zeros(starts[d+1],dtype=np.int8);A[0]=1
 for a in w:
  i=abs(a)-1
  for k in (range(d,0,-1) if a>0 else range(1,d+1)):
   # All words of length k with final letter i, versus their prefixes.
   dest=slice(starts[k]+i,starts[k+1],3);src=slice(starts[k-1],starts[k])
   A[dest]=(A[dest]+(1 if a>0 else -1)*A[src])%p
 return A

def seeds():
 G=[]
 for i in range(1,4):
  for j in range(1,4):
   if i!=j:G.append(K(3,i,j))
  js=[j for j in range(1,4) if j!=i];G.append(C(3,i,*js))
 G2=[]
 for (a,ai),(b,bi) in product(G,repeat=2):
  h=auto_commutator(a,ai,b,bi);hi=auto_commutator(b,bi,a,ai);G2.append((h,hi))
 G3=[]
 for (a,ai),(b,bi) in product(G2,G):G3.append(auto_commutator(a,ai,b,bi))
 N=(3**9-1)//2
 out=np.zeros((len(G3),3,N),dtype=np.int8)
 cache={};t=time.time()
 for k,g in enumerate(G3):
  for i,w in enumerate(g):
   if w not in cache:cache[w]=expand(w)
   out[k,i]=cache[w]
   out[k,i,0]-=1;out[k,i,1+i]-=1;out[k,i]%=9
  assert not out[k,:,:40].any() # no displacement degree<4
  if k%100==0:print(k,'elapsed',time.time()-t,flush=True)
 np.savez_compressed('workspace/agent3_mod9_gamma3_tensor_seeds.npz',seeds=out[:,:,(3**4-1)//2:])
 print('saved',out.shape,'elapsed',time.time()-t)
 return out
if __name__=='__main__':seeds()
