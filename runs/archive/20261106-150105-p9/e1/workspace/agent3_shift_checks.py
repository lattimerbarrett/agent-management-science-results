import numpy as np, time, json

class Model:
 def __init__(self,Q,depth,t=1):
  self.Q=Q; self.depth=depth; self.left=[]; self.right=[]; self.nodelevels=[]; self.leafnodes=[]; self.mats=[]
  b=np.sqrt(t/Q); total=(5+b*b-1/Q)/2; disc=total**2-4*(1+b*b)
  self.a=(total+np.sqrt(disc))/2; self.c=(total-np.sqrt(disc))/2; self.b=b
  self.root=self.branch(np.diag([Q,1.]),depth,0)
  self.left=np.array(self.left,dtype=int); self.right=np.array(self.right,dtype=int); self.nodelevels=np.array(self.nodelevels); self.leafnodes=np.array(self.leafnodes,dtype=int)
  self.levels=[np.where((self.nodelevels==i)&(self.left>=0))[0] for i in range(max(self.nodelevels)+1)]
  self.internal=np.where(self.left>=0)[0]
  ds,Us=np.linalg.eigh(self.mats); ds=np.maximum(ds,1e-300)
  self.F=np.einsum('nik,nk,njk->nij',Us,np.sqrt(ds),Us); self.B=np.einsum('nik,nk,njk->nij',Us,1/np.sqrt(ds),Us)
 def node(self,l,r,level,W=None):
  n=len(self.left); self.left.append(l);self.right.append(r);self.nodelevels.append(level)
  if l<0:self.leafnodes.append(n); self.mats.append(W)
  return n
 def frozen(self,W,level,extra=2):
  if not extra:return self.node(-1,-1,level,W)
  l=self.frozen(W,level+1,extra-1);r=self.frozen(W,level+1,extra-1)
  return self.node(l,r,level)
 def branch(self,W,depth,level):
  d,U=np.linalg.eigh(W); d=d[::-1];U=U[:,::-1]
  # preserve determinant in the factorization despite anisotropy
  d[1]=self.Q/d[0]; G=U@np.diag(np.sqrt(d))
  if depth==0:
   b=np.sqrt(1-1/self.Q)
   P=G@np.array([[1.,b],[b,1.]])@G.T; M=G@np.array([[1.,-b],[-b,1.]])@G.T
   l=self.frozen(P,level+1);r=self.frozen(M,level+1)
   return self.node(l,r,level)
  P=G@np.array([[self.a,self.b],[self.b,self.c]])@G.T
  M=G@np.array([[self.a,-self.b],[-self.b,self.c]])@G.T
  L=G@np.diag([2-self.a,2-self.c])@G.T
  p=self.branch(P,depth-1,level+2); l=self.frozen(L,level+2)
  m=self.branch(M,depth-1,level+2); r=self.frozen(L,level+2)
  left=self.node(p,l,level+1);right=self.node(m,r,level+1)
  return self.node(left,right,level)
 def haar(self,v):
  vals=np.zeros((len(self.left),2)); coeff=np.zeros_like(vals);vals[self.leafnodes]=v
  for ids in self.levels[::-1]:
   vl=vals[self.left[ids]];vr=vals[self.right[ids]]
   vals[ids]=(vl+vr)/np.sqrt(2);coeff[ids]=(vl-vr)/np.sqrt(2)
  return coeff
 def invhaar(self,coeff):
  vals=np.zeros_like(coeff)
  for ids in self.levels:
   vals[self.left[ids]]=(vals[ids]+coeff[ids])/np.sqrt(2)
   vals[self.right[ids]]=(vals[ids]-coeff[ids])/np.sqrt(2)
  return vals[self.leafnodes]
 def shift(self,v,adj=False):
  coeff=self.haar(v);out=np.zeros_like(coeff);ids=self.internal
  if adj:
   out[ids]=(coeff[self.left[ids]]-coeff[self.right[ids]])/np.sqrt(2)
  else:
   out[self.left[ids]]=coeff[ids]/np.sqrt(2);out[self.right[ids]]=-coeff[ids]/np.sqrt(2)
   out[self.leafnodes]=0
  return self.invhaar(out)
 def T(self,v,adj=False):
  if not adj:return np.einsum('nij,nj->ni',self.F,self.shift(np.einsum('nij,nj->ni',self.B,v)))
  return np.einsum('nij,nj->ni',self.B,self.shift(np.einsum('nij,nj->ni',self.F,v),True))
 def norm(self,iters=70):
  rng=np.random.default_rng(5);v=rng.normal(size=(len(self.leafnodes),2));v/=np.linalg.norm(v)
  # Verify adjoint implementation.
  w=rng.normal(size=v.shape)
  assert abs(np.sum(self.T(v)*w)-np.sum(v*self.T(w,True)))<1e-7*np.linalg.norm(w)
  for i in range(iters):
   z=self.T(self.T(v),True);v=z/np.linalg.norm(z)
  return np.linalg.norm(self.T(v))

results=[]
for Q,d in [(2.,6),(3.,8),(4.,10),(4.,14),(8.,10),(8.,14),(16.,14)]:
 t=time.time();m=Model(Q,d);n=m.norm();r={'Q':Q,'depth':d,'leaves':len(m.leafnodes),'shift_norm_lower':n,'ratio_to_Q32':n/Q**1.5,'seconds':time.time()-t};print(r,flush=True);results.append(r)
with open('workspace/agent3_shift_results.json','w') as f:json.dump(results,f,indent=2)
with open('workspace/agent3_shift_checks.py','w') as f:f.write(open('scratchpad.py').read())
