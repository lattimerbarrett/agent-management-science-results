import numpy as np
from collections import deque,Counter
import time,json

def run(n,L):
 q=2**L;I=np.eye(n,dtype=np.int64)
 def mul(a,b):return (a@b)%q
 def inv(a):
  u=(I-a)%q;s=I.copy();p=I.copy()
  for k in range(1,L):p=mul(p,u);s=(s+p)%q
  assert np.array_equal(mul(a,s),I)
  return s
 def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
 def pivot(a):
  d=(a-I)%q;out=[]
  for i in range(n):
   for j in range(n):
    x=int(d[i,j])
    if x:out.append(((x&-x).bit_length()-1,i,j))
  return min(out) if out else None
 G=[];labels=[]
 for i in range(n):
  for j in range(n):
   if i==j:continue
   a=I.copy();a[i,i]=-1;a[i,j]=2;G.append(a.T%q);labels.append(('K',i,j))
  for j in range(n):
   for k in range(j+1,n):
    if i in (j,k):continue
    a=I.copy();a[i,j]=2;a[i,k]=-2;G.append(a.T%q);labels.append(('C',i,j,k))
 class GS:
  def __init__(self):self.basis={};self.invs={}
  def sift(self,a,insert=True):
   while True:
    z=pivot(a)
    if z is None:return None
    if z not in self.basis:
     if insert:self.basis[z]=a;self.invs[z]=inv(a)
     return a
    a=mul(a,self.invs[z])
  def close(self,seeds):
   Q=deque(seeds)
   while Q:
    a=self.sift(Q.popleft())
    if a is not None:
     Q.append(mul(a,a));Q.extend(comm(g,a) for g in G)
   return self
 H=GS().close(G);last=H;dims=[len(H.basis)]
 a=G[labels.index(('K',0,1))];b=G[labels.index(('C',0,1,2))];c=G[labels.index(('C',2,0,1))]
 w=comm(a,comm(b,c))
 print('n,L',n,L,'w!=I',not np.array_equal(w,I),'wval',pivot(w),flush=True)
 for degree in range(2,5):
  last=GS().close(comm(g,h) for g in G for h in last.basis.values());dims.append(len(last.basis))
 print('dims',dims,'w not gamma4',last.sift(w,False) is not None,flush=True)
 return [n,L,dims,last.sift(w,False) is not None]
if __name__=='__main__':
 out=[run(n,L) for n in [3,4,5] for L in [5,7,9]]
 json.dump(out,open('workspace/agent2_fox_results.json','w'))
