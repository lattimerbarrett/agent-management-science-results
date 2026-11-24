from collections import deque,Counter
import time,json
p=2;n=3;M=5

def add(a,b):return a^b
ONE={()}
X=[{(i,)} for i in range(n)]
def mul(a,b):
 d=set()
 for u in a:
  for v in b:
   if len(u)+len(v)<=M:
    w=u+v
    if w in d:d.remove(w)
    else:d.add(w)
 return d
def ex(i,sign=1):return {(),(i,)} if sign==1 else {(i,)*k for k in range(M+1)}
def groupword(w):
 a=ONE
 for i,s in w:a=mul(a,ex(i,s))
 return a

def subs(a,images):
 d=set()
 for w in a:
  t=ONE
  for i in w:t=mul(t,images[i])
  d^=t
 return d

def compose(A,B):return [subs(b,A) for b in B]
def inverse(A):
 ans=[]
 for i in range(n):
  t=X[i];s=set(t)
  for k in range(1,M):
   t=subs(t,A)^t;s^=t
  ans.append(s)
 return ans

def comm(A,B):return compose(compose(compose(A,B),inverse(A)),inverse(B))
def pivot(A):
 z=[(len(w),i,w) for i in range(n) for w in A[i]^X[i]]
 return min(z) if z else None
G=[]
for i in range(n):
 for j in range(n):
  if i==j:continue
  images=X.copy();images[i]=groupword([(j,1),(i,1),(j,-1)])^ONE;G.append(images)
 for j in range(n):
  for k in range(j+1,n):
   if i in (j,k):continue
   images=X.copy();images[i]=groupword([(i,1),(j,1),(k,1),(j,-1),(k,-1)])^ONE;G.append(images)
assert all(compose(g,inverse(g))==X for g in G)

class GroupSpace:
 def __init__(self):self.basis={};self.inverses={}
 def sift(self,A):
  while True:
   z=pivot(A)
   if z is None:return None
   if z not in self.basis:
    self.basis[z]=A;self.inverses[z]=inverse(A);return A
   A=compose(A,self.inverses[z])
 def close(self,seeds):
  q=deque(seeds);tic=time.time()
  while q:
   a=self.sift(q.popleft())
   if a is not None:
    q.append(compose(a,a))
    q.extend(comm(g,a) for g in G)
    if len(self.basis)%20==0:print(' rank',len(self.basis),'queue',len(q),'time',round(time.time()-tic,2),flush=True)
  return self
 def rank(self):return len(self.basis)

H=GroupSpace().close(G)
print('H rank',H.rank(),Counter(z[0] for z in H.basis),flush=True)
last=H
results=[]
for c in range(2,M):
 T=GroupSpace().close(comm(g,h) for g in G for h in last.basis.values())
 print('gamma',c,'rank',T.rank(),'graded',dict(Counter(z[0] for z in T.basis)),flush=True)
 results.append([c,T.rank(),dict(Counter(z[0] for z in T.basis))]);last=T
json.dump(results,open('workspace/agent3_pgroup_results.json','w'))
open('workspace/agent3_pgroup.py','w').write(open(__file__).read())
