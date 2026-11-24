import numpy as np,time,json
# Reuse only checked Haar tree matvec definitions, excluding original runs.
exec(open('workspace/agent3_shift_checks.py').read().split('results=[]')[0])

class TriangularModel(Model):
 def __init__(self,p,K,depth,eps=.2):
  self.p=p;self.q=p/(p-1);self.K=K;self.depth=depth
  self.beta=(.5-eps/K)/p;self.eta=(.5-eps/K**(1/(p-1)))/self.q;self.Tval=4**(-self.beta-self.eta);self.lam=K**(-1/p)
  self.left=[];self.right=[];self.nodelevels=[];self.leafnodes=[];self.mats=[]
  self.root=self.tribranch(0,0.,1.,depth,0)
  self.left=np.array(self.left,dtype=int);self.right=np.array(self.right,dtype=int);self.nodelevels=np.array(self.nodelevels);self.leafnodes=np.array(self.leafnodes,dtype=int)
  self.levels=[np.where((self.nodelevels==i)&(self.left>=0))[0] for i in range(max(self.nodelevels)+1)];self.internal=np.where(self.left>=0)[0]
  self.F=np.array(self.mats);self.B=np.linalg.inv(self.F)
  self.length=2.**(-self.nodelevels[self.leafnodes]);D=self.length**(1/p-.5)
  self.F*=D[:,None,None];self.B/=D[:,None,None]
 def tribbranch(self,*args):return self.tribranch(*args)
 def tribranch(self,n,offset,scale,depth,level):
  u=self.lam*4**(self.beta*n);v=4**(-self.eta*n);F=np.array([[u,u*(offset+.5*scale)],[0.,v]])
  if depth==0:return self.frozen(F,level)
  t=self.Tval
  p=self.tribranch(n+1,offset,scale*t,depth-1,level+2);l=self.frozen(F,level+2)
  m=self.tribranch(n+1,offset+scale*(1-t),scale*t,depth-1,level+2);r=self.frozen(F,level+2)
  left=self.node(p,l,level+1);right=self.node(m,r,level+1)
  return self.node(left,right,level)
 def lp(self,v,r):return np.sum(np.linalg.norm(v,axis=1)**r)**(1/r)
 def dualitymap(self,v,r):return v*np.maximum(np.linalg.norm(v,axis=1),1e-200)[:,None]**(r-2)
 def normp(self,iters=100):
  rng=np.random.default_rng(44);v=rng.normal(size=(len(self.leafnodes),2));v/=self.lp(v,self.p)
  for i in range(iters):
   z=self.T(self.dualitymap(self.T(v),self.p),True);v=self.dualitymap(z,self.q);v/=self.lp(v,self.p)
  return self.lp(self.T(v),self.p)

results=[]
for p in [2.,3.,4.]:
 for K in [2.,4.,8.,16.]:
  t=time.time();m=TriangularModel(p,K,10);n=m.normp(100);r={'p':p,'K':K,'depth':10,'T':m.Tval,'norm_lower':float(n),'ratio_alpha':float(n/K**(1+1/(p*(p-1)))),'seconds':time.time()-t};print(r,flush=True);results.append(r)
with open('workspace/agent3_overlap_shift_results.json','w') as f:json.dump(results,f,indent=2)
with open('workspace/agent3_overlap_shift_checks.py','w') as f:f.write(open('scratchpad.py').read())
