import itertools, numpy as np, scipy.sparse as sp, json, time
from collections import defaultdict
N=7; p=1009; nv=3
words=[w for d in range(2,N+1) for w in itertools.product(range(nv),repeat=d)]
keys=[(i,w) for i in range(nv) for w in words]; index={k:j for j,k in enumerate(keys)}; dim=len(keys)
def add(a,b,sgn=1):
 c=a.copy()
 for w,v in b.items():
  c[w]=(c.get(w,0)+sgn*v)%p
  if not c[w]:del c[w]
 return c
def scale(a,v):return {w:t*v%p for w,t in a.items() if t*v%p}
def mul(a,b):
 c=defaultdict(int)
 for w,x in a.items():
  for u,y in b.items():
   if len(w)+len(u)<=N:c[w+u]=(c[w+u]+x*y)%p
 return {w:x for w,x in c.items() if x}
def log(a):
 b=add(a,{():1},-1); c={};q={():1}
 for k in range(1,N+1):
  q=mul(q,b);c=add(c,scale(q,((-1)**(k+1)*pow(k,-1,p))%p))
 return c
one={():1}; X=[{(i,):1} for i in range(nv)]; gx=[add(one,x) for x in X]
inv=[]
for i in range(nv):inv.append({(i,)*k:(-1)**k%p for k in range(N+1)})
gens=[]
for i in range(nv):
 for j in range(nv):
  if i==j:continue
  l=log(gx[j]); im=add(mul(l,X[i]),mul(X[i],l),-1);D=[{}, {}, {}];D[i]=im;gens.append(D)
for i in range(nv):
 j,k=[v for v in range(nv) if v!=i]
 w=mul(mul(mul(gx[j],gx[k]),inv[j]),inv[k]);l=log(w);D=[{},{},{}];D[i]=mul(l,gx[i]);gens.append(D)
def vect(D):
 v=np.zeros(dim,dtype=np.int64)
 for i,pol in enumerate(D):
  for w,c in pol.items():v[index[i,w]]=c
 return v

def act(D,word):
 out={}
 for j,k in enumerate(word):
  for u,c in D[k].items():
   w=word[:j]+u+word[j+1:]
   if len(w)<=N:out[w]=(out.get(w,0)+c)%p
 return out
ads=[]
for D in gens:
 rr=[];cc=[];vv=[]
 for col,(i,w) in enumerate(keys):
  for u,c in act(D,w).items():rr.append(index[i,u]);cc.append(col);vv.append(c)
  # E sends X_i -> w, acting on every output of D
  for j in range(nv):
   for u,c in D[j].items():
    for pos,a in enumerate(u):
     if a==i:
      z=u[:pos]+w+u[pos+1:]
      if len(z)<=N:rr.append(index[j,z]);cc.append(col);vv.append(-c)
 ads.append(sp.csr_matrix((vv,(rr,cc)),shape=(dim,dim),dtype=np.int64))
class Span:
 def __init__(self):self.rows={}
 def add(self,v):
  v=v.copy()%p
  while np.any(v):
   i=int(np.flatnonzero(v)[0])
   if i in self.rows:v=(v-v[i]*self.rows[i])%p
   else:
    v=v*pow(int(v[i]),-1,p)%p;self.rows[i]=v;return True
  return False
 def basis(self):return list(self.rows.values())
bs={1:[vect(D) for D in gens]}
for k in range(2,N+1):
 S=Span()
 for v in bs[k-1]:
  for A in ads:S.add(A@v)
 bs[k]=S.basis();print('exact bracket length',k,'rank',len(bs[k]),flush=True)
S4=Span();S5=Span();T=Span()
for k in range(N-1,3,-1):
 for v in bs[k]:
  S4.add(v)
  if k>=5:S5.add(v)
for v in bs[4]:
 w=v.copy();w[np.array([len(u)!=5 for i,u in keys])]=0;T.add(w)
print('gamma4',len(S4.rows),'gamma5',len(S5.rows),'lead4',len(T.rows),'defect',len(S4.rows)-len(S5.rows)-len(T.rows))
