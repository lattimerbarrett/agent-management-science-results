from collections import defaultdict
from itertools import product,combinations
from pathlib import Path
from sage.all import matrix,ZZ,GF
import time,json
n=3

def add(a,b,s=1):
 d=a.copy()
 for w,v in b.items():
  d[w]=d.get(w,0)+s*v
  if not d[w]:del d[w]
 return d

def mul(a,b):
 d={}
 for u,x in a.items():
  for v,y in b.items():
   w=u+v;d[w]=d.get(w,0)+x*y
 return {w:v for w,v in d.items() if v}
def comm(a,b):return add(mul(a,b),mul(b,a),-1)
X=[{(i,):1} for i in range(n)]
zero=lambda:[{} for _ in range(n)]
def dadd(D,E):return [add(d,e) for d,e in zip(D,E)]
def deriv(D,a):
 d={}
 for w,v in a.items():
  for k,i in enumerate(w):
   for u,z in D[i].items():
    ww=w[:k]+u+w[k+1:];d[ww]=d.get(ww,0)+v*z
 return {w:v for w,v in d.items() if v}
def br(D,E):return [add(deriv(D,E[i]),deriv(E,D[i]),-1) for i in range(n)]
def flat(D):return {(i,w):v for i,a in enumerate(D) for w,v in a.items()}
G=[];J=[];names=[]
for i in range(n):
 for j in range(n):
  if i==j:continue
  D=zero();D[i]=comm(X[j],X[i]);G.append(D);J.append(zero());names.append(('K',i,j))
 for j,k in combinations(range(n),2):
  if i in (j,k):continue
  D=zero();C=comm(X[j],X[k]);D[i]=C
  E=zero();E[i]=comm(add(add(X[j],X[k]),X[i]),C)
  G.append(D);J.append(E);names.append(('C',i,j,k))
pairs=list(combinations(range(9),2))
B={(j,k):br(G[j],G[k]) for j,k in pairs}
T=[];V=[]
for i in range(9):
 for j,k in pairs:
  t=br(G[i],B[j,k]);T.append(t)
  v=dadd(br(J[i],B[j,k]),br(G[i],dadd(br(J[j],G[k]),br(G[j],J[k]))))
  v=dadd(v,br(G[i],br(dadd(G[j],G[k]),B[j,k])))
  v=dadd(v,br(G[i],t));V.append(v)
print('built triple',flush=True)
keys3=[(i,w) for i in range(n) for w in product(range(n),repeat=4)]
keys4=[(i,w) for i in range(n) for w in product(range(n),repeat=5)]
ix3={k:i for i,k in enumerate(keys3)};ix4={k:i for i,k in enumerate(keys4)}
def mat(cols,ix,ring=ZZ):
 return matrix(ring,len(ix),len(cols),{(ix[k],j):v for j,c in enumerate(cols) for k,v in flat(c).items()},sparse=True)
A=mat(T,ix3);print('rank3',A.rank(),flush=True)
K=A.right_kernel_matrix();print('integer kernel',K.nrows(),K.ncols(),flush=True)
Vmat=mat(V,ix4)
R=Vmat*K.transpose()
assert all(x%2==0 for x in R.list())
R=matrix(ZZ,R.nrows(),R.ncols(),[x//2 for x in R.list()])
print('quartic relation image built',flush=True)
Lcols=[br(g,t) for g in G for t in T]
L=mat(Lcols,ix4)
for p in [2,3,5,101]:
 l=L.change_ring(GF(p));r=R.change_ring(GF(p));a=l.augment(r)
 rl=l.rank();ra=a.rank();print('prime',p,'Lrank',rl,'augmented',ra,flush=True)
Path('workspace/agent4_lattice.py').write_text(Path('scratchpad.py').read_text())
A.save('workspace/agent4_D3');K.save('workspace/agent4_K');R.save('workspace/agent4_R4');L.save('workspace/agent4_L4')
