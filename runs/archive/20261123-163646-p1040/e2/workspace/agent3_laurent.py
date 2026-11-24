import numpy as np,time,json
from collections import deque,Counter
p=3;m=3;L=7
I=np.zeros((L,m,m),dtype=np.int64);I[0]=np.eye(m,dtype=np.int64)
def mul(A,B):
 C=np.zeros_like(I)
 for i in range(L):
  for j in range(L-i):C[i+j]+=A[i]@B[j]
 return C%p
def inv(A):
 B=(I-A)%p;C=I.copy();D=I.copy()
 for k in range(1,L):D=mul(D,B);C=(C+D)%p
 return C
def comm(A,B):return mul(mul(mul(A,B),inv(A)),inv(B))
def power(A,k):
 C=I
 for _ in range(k):C=mul(C,A)
 return C
def pivot(A):
 z=np.flatnonzero((A-I).reshape(-1)%p)
 return int(z[0]) if len(z) else None
G=[]
for i in range(m):
 A=I.copy();A[1,i,i]=1;G.append(A)
 for j in range(m):
  if i==j:continue
  A=I.copy();A[1,i,j]=1;G.append(A)
class Space:
 def __init__(self):self.rows={};self.inverse={}
 def sift(self,A):
  while True:
   k=pivot(A)
   if k is None:return False
   v=int(A.reshape(-1)[k])
   if k not in self.rows:
    A=power(A,pow(v,-1,p));self.rows[k]=A;self.inverse[k]=inv(A);return A
   A=mul(A,power(self.inverse[k],v))
 def close(self,seeds):
  q=deque(seeds)
  while q:
   A=self.sift(q.popleft())
   if A is not False:
    q.append(power(A,p));q.extend(comm(g,A) for g in G)
  return self
H=Space().close(G)
print('H',len(H.rows),Counter(k//(m*m) for k in H.rows),flush=True)
last=H
for c in range(2,L):
 H=Space().close(comm(g,A) for g in G for A in last.rows.values())
 print('gamma',c,len(H.rows),Counter(k//(m*m) for k in H.rows),flush=True)
 last=H
open('workspace/agent3_laurent.py','w').write(open(__file__).read())
