import itertools, numpy as np, scipy.sparse as sp, json, time
from collections import defaultdict
N=6; p=1009; nv=3
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
S5=Span()
for v in bs[5]:S5.add(v)
S4=Span()
for k in [5,4]:
 for v in bs[k]:S4.add(v)
Slead=Span();mask=np.array([len(w)!=5 for i,w in keys])
for v in bs[4]:
 v=v.copy();v[mask]=0;Slead.add(v)
print('gamma4dim gamma5dim leading4rank defect',len(S4.rows),len(S5.rows),len(Slead.rows),len(S4.rows)-len(S5.rows)-len(Slead.rows))
for k in range(1,6):
 T=Span();mask=np.array([len(w)!=k+1 for i,w in keys])
 for v in bs[k]:
  v=v.copy();v[mask]=0;T.add(v)
 print('Johnson degree',k,'rank',len(T.rows))
import shutil
# Integral class-five group commutator detection modulo 2.
def signlift(x):return int(x) if x<=p//2 else int(x)-p
g1=[];g2=[]
for D in gens:
 v=vect(D);a=np.zeros(dim,dtype=np.int64);b=a.copy()
 for j,(i,w) in enumerate(keys):
  if len(w)==2:a[j]=signlift(v[j])
  if len(w)==3:b[j]=signlift((2*v[j])%p)
 g1.append(a);g2.append(b)
def admat(v):
 D=[{} for _ in range(3)]
 for j,(i,w) in enumerate(keys):
  if v[j]:D[i][w]=int(v[j])
 rr=[];cc=[];vv=[]
 for col,(i,w) in enumerate(keys):
  for u,c in act(D,w).items():rr.append(index[i,u]);cc.append(col);vv.append(signlift(c))
  for j in range(nv):
   for u,c in D[j].items():
    for pos,a in enumerate(u):
     if a==i:
      z=u[:pos]+w+u[pos+1:]
      if len(z)<=N:rr.append(index[j,z]);cc.append(col);vv.append(-c)
 return sp.csr_matrix((vv,(rr,cc)),shape=(dim,dim),dtype=np.int64)
a1=[admat(v) for v in g1];a2=[admat(v) for v in g2]
class BitSpan:
 def __init__(self):self.rows={}
 def add(self,v):
  z=0
  for j in np.flatnonzero(v%2):z|=1<<int(j)
  while z:
   k=z.bit_length()-1
   if k in self.rows:z^=self.rows[k]
   else:self.rows[k]=z;return True
  return False
pairs=[(g1[i],g2[i],i) for i in range(9)]
for k in range(2,5):
 nxt=[]
 for lead,tail,old in pairs:
  for i in range(9):
   l=a1[i]@lead;t=a2[i]@lead+a1[i]@tail+a1[i]@l
   if k==2:t+=a1[old]@l
   nxt.append((l,t,-1))
 pairs=nxt
 print('integer commutators length',k,'count',len(pairs),flush=True)
L5=BitSpan()
for v in bs[5]:pass
# Obtain homogeneous length4 spanning set over F2, retaining actual vectors.
b4=BitSpan();leads=[]
for l,t,_ in pairs:
 if b4.add(l):leads.append(l)
for l in leads:
 for A in a1:L5.add(A@l)
L45=BitSpan();L45.rows=L5.rows.copy();bad=0
for l,t,_ in pairs:
 if np.any(t%2):bad+=1
 L45.add(l+t//2)
print('integral pair odd tails',bad,'L4lead mod2',len(b4.rows),'L5mod2',len(L5.rows),'L45mod2',len(L45.rows),'difference',len(L45.rows)-len(L5.rows))
