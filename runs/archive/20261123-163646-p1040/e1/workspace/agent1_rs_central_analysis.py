"""RS class3 upper bound allowing unknown central γ3 edge tails.
Depends on proved A3=γ3, checked degree2 certificate, and genuine AutF3 presentation.
"""
import json,time
import numpy as np
from sage.all import Matrix,ZZ,GF
from agent1_degree3 import expand,coords,L3,ld,N
from agent1_degree3_closure import row_basis
from agent1_peiffer_c3 import inv

M=9
ZERO=(np.zeros(M,dtype=np.int64),np.zeros((M,M),dtype=np.int64),np.zeros((M,M,M),dtype=np.int64))
def poly(w):
 p=expand(w);out=tuple(a.copy() for a in ZERO)
 for t,x in p.items():
  if t:out[len(t)-1][t]=int(x)
 return out

def pmul(P,Q):
 a,b,c=P;d,e,f=Q
 return (a+d,b+e+np.einsum('i,j->ij',a,d),c+f+np.einsum('i,jk->ijk',a,e)+np.einsum('ij,k->ijk',b,d))

class Eliminator:
 def __init__(self,p,projection,Bfree,needed):
  self.p=p;self.proj=projection;self.Bfree=Bfree;self.needed=needed;self.unknown={};self.known={};self.rows=0
 def known_insert(self,v):
  p=self.p
  while np.any(v):
   k=int(np.flatnonzero(v)[0]);c=int(v[k])
   if k in self.known:v=(v-c*self.known[k])%p
   else:
    v=v*pow(c,-1,p)%p
    assert not np.any(v@self.Bfree%p),'invalid known relation image'
    self.known[k]=v
    print('NEW valid cubic relation mod',p,'count',len(self.known),'needed',self.needed,flush=True)
    return
 def insert(self,z,v):
  p=self.p;v=np.asarray(v,dtype=np.int64)@self.proj%p
  z={k:x%p for k,x in z.items() if x%p};self.rows+=1
  while z:
   k=min(z);c=z[k]
   if k not in self.unknown:
    a=pow(c,-1,p);z={j:x*a%p for j,x in z.items()};v=v*a%p
    self.unknown[k]=(z,v);return
   dz,dv=self.unknown[k]
   for j,x in dz.items():
    z[j]=(z.get(j,0)-c*x)%p
    if not z[j]:del z[j]
   v=(v-c*dv)%p
  self.known_insert(v)

def analyze(edgepaths,cache,ident,gs,gis):
 from agent2_edge_preimage import preimage as edge_preimage_mod_gamma3
 H=Matrix(ZZ,json.load(open('workspace/agent1_class3_HNF215.json')))
 Hn=np.array(H.rows(),dtype=np.int64);A=H[:18,:36];piv=A.pivots()
 Ai=np.array(A[:,piv].inverse().rows(),dtype=np.int64)
 C=H[:,:36].transpose().right_kernel().basis_matrix()*H[:,36:]
 assert all(x%2==0 for x in C.list())
 C=row_basis(C.apply_map(lambda x:x//2))
 keys=[(i,w) for i in range(N) for w in __import__('itertools').product(range(N),repeat=4)]
 B=Matrix(ZZ,[[ld(w)[i].get(t,0) for w in L3] for i,t in keys])
 eliminators=[]
 for p in (2,3):
  E=Matrix(GF(p),C).echelon_form();r=E.rank();E=E[:r,:];pc=list(E.pivots());fc=[j for j in range(240) if j not in pc]
  P=np.zeros((240,len(fc)),dtype=np.int64)
  for j,k in enumerate(fc):P[k,j]=1
  for i,k in enumerate(pc):P[k,:]=-np.array([int(E[i,j]) for j in fc],dtype=np.int64)%p
  Bfree=np.array(B[:,fc].transpose().rows(),dtype=np.int64)%p
  eliminators.append(Eliminator(p,P,Bfree,197-r))
 unknowns={};polys={};wordlength={};started=time.time()
 def ep(f,fi):
  if f in polys:return polys[f]
  if f in cache:w=cache[f];key=None;sgn=0
  elif fi in cache:w=inv(cache[fi]);key=None;sgn=0
  else:
   key=min(f,fi);sgn=1 if f==key else -1
   if key not in unknowns:
    unknowns[key]=len(unknowns)
   base=edge_preimage_mod_gamma3(key)
   w=base if sgn==1 else inv(base)
   key=unknowns[key]
  out=(poly(w),len(w),key,sgn);polys[f]=out
  return out
 for idx,edges in enumerate(edgepaths):
  P=ZERO;z={};L=0
  for f,fi in edges:
   Q,n,k,s=ep(f,fi);L+=n;assert L<1000000,'int64 bound'
   P=pmul(P,Q)
   if k is not None:z[k]=z.get(k,0)+s
  if not z:continue # all exact-word loops already checked against H in prior certificates
  assert not np.any(P[0])
  r2=P[1];p3=2*P[2].copy()
  for i in range(M):
   for j in range(M):
    p3[i,i,j]+=r2[i,j];p3[i,j,j]+=r2[i,j]
  q2=np.array([r2[i,j] for i in range(M) for j in range(i+1,M)],dtype=np.int64)
  c=q2[list(piv)]@Ai
  assert np.array_equal(q2,c@Hn[:18,:36])
  d=coords({t:int(p3[t]) for t in __import__('itertools').product(range(M),repeat=3) if p3[t]})
  v=np.array(d,dtype=np.int64)-c@Hn[:18,36:]
  assert not np.any(v%2)
  v=v//2
  for el in eliminators:el.insert(z,v)
  if idx%500==0:print('RScentral loop',idx,'unknowns',len(unknowns),'newranks',[len(el.known) for el in eliminators],'seconds',round(time.time()-started,2),flush=True)
 print('RESULT loops',len(edgepaths),'unknowns',len(unknowns),'new relation ranks',[len(el.known) for el in eliminators],'needed',[el.needed for el in eliminators],flush=True)
 if all(len(el.known)==el.needed for el in eliminators):print('PASS integral degree3 IA3 Johnson injectivity')
 else:print('INCOMPLETE RScentral certificate')
 return eliminators
