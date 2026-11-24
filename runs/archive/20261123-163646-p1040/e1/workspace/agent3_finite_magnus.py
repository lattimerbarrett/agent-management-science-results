import numpy as np
from itertools import product
class MagnusRing:
 def __init__(self,d=7,p=3):
  self.d=d;self.p=p
  self.mons=[a for k in range(d+1) for a in product(range(k+1),repeat=3) if sum(a)==k]
  self.idx={a:i for i,a in enumerate(self.mons)};self.deg=np.array(list(map(sum,self.mons)))
  self.N=len(self.mons);self.z=np.zeros((self.N,3,3),dtype=np.int64)
  self.mulidx=np.full((self.N,self.N),-1,dtype=int)
  for i,a in enumerate(self.mons):
   for j,b in enumerate(self.mons):
    c=tuple(x+y for x,y in zip(a,b))
    if sum(c)<=d:self.mulidx[i,j]=self.idx[c]
 def mul(self,A,B):
  ia=np.flatnonzero(np.any(A,axis=(1,2)));ib=np.flatnonzero(np.any(B,axis=(1,2)))
  C=self.z.copy()
  if not len(ia) or not len(ib):return C
  ids=self.mulidx[np.ix_(ia,ib)];r,s=np.where(ids>=0)
  if len(r):np.add.at(C,ids[r,s],np.matmul(A[ia[r]],B[ib[s]]))
  return C%self.p
 def inv(self,A):
  C=self.z.copy();power=A.copy();sgn=-1
  for k in range(1,self.d+1):
   C=(C+sgn*power)%self.p
   power=self.mul(power,A)
   if not power.any():break
   sgn=-sgn
  return C
 def comm(self,A,B,Bi=None):
  C=(self.mul(A,B)-self.mul(B,A))%self.p
  if not C.any():return C
  C=(C+self.mul(C,self.inv(A)))%self.p
  return (C+self.mul(C,self.inv(B) if Bi is None else Bi))%self.p
 def scalar(self,exps):
  C=self.z.copy()
  for a,v in exps.items():C[self.idx[a]]=np.eye(3,dtype=int)*v
  return C%self.p
 def generators(self):
  # Abelianized Fox Jacobian, columns = changed images; IA composition
  # induces matrix multiplication up to opposite convention, irrelevant here.
  gs=[]
  for i in range(3):
   for j in range(3):
    if i==j:continue
    A=self.z.copy();ej=tuple(int(k==j) for k in range(3));ei=tuple(int(k==i) for k in range(3))
    A[self.idx[ej],i,i]+=1;A[self.idx[ei],j,i]-=1;gs.append(A%self.p)
   js=[j for j in range(3) if j!=i];j,k=js
   A=self.z.copy()
   ej=tuple(int(t==j) for t in range(3));ek=tuple(int(t==k) for t in range(3));ei=tuple(int(t==i) for t in range(3))
   eik=tuple(x+y for x,y in zip(ei,ek));eij=tuple(x+y for x,y in zip(ei,ej))
   A[self.idx[ek],j,i]-=1;A[self.idx[eik],j,i]-=1
   A[self.idx[ej],k,i]+=1;A[self.idx[eij],k,i]+=1;gs.append(A%self.p)
  return gs
class Span:
 def __init__(self,R):self.R=R;self.basis={}
 def add(self,A):
  v=A.reshape(-1).copy()%self.R.p
  for pivot,b in sorted(self.basis.items()):
   if v[pivot]:v=(v-v[pivot]*b)%self.R.p
  nz=np.flatnonzero(v)
  if not len(nz):return None
  pivot=int(nz[0]);v=v*pow(int(v[pivot]),-1,self.R.p)%self.R.p
  self.basis[pivot]=v
  return v.reshape(A.shape)
 def arrays(self):return [b.reshape(self.R.z.shape) for b in self.basis.values()]


def verify():
 import time
 t=time.time();R=MagnusRing();gs=R.generators();gis=[R.inv(g) for g in gs]
 levels=[gs]
 for k in (2,3):levels.append([R.comm(a,b,bi) for a in levels[-1] for b,bi in zip(gs,gis)])
 S=Span(R)
 for a in levels[-1]:
  for b,bi in zip(gs,gis):S.add(R.comm(a,b,bi))
 def close(S):
  queue=S.arrays();cur=0
  while cur<len(queue):
   a=queue[cur];cur+=1
   for b,bi in zip(gs,gis):
    v=S.add(R.comm(a,b,bi))
    if v is not None:queue.append(v)
  return S
 S=close(S);print('gamma4 dimension',len(S.basis))
 for c in (5,6,7):
  T=Span(R)
  for a in S.arrays():
   for b,bi in zip(gs,gis):T.add(R.comm(a,b,bi))
  T=close(T);lead=Span(R)
  for a in T.arrays():
   v=a.copy();v[R.deg!=c]=0;lead.add(v)
  print('gamma',c,'dimension',len(T.basis),'leading degree rank',len(lead.basis))
  S=T
 print('elapsed',time.time()-t)
if __name__=='__main__':verify()
