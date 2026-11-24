import numpy as np

def kappa_rows(bi):
 gap=bi.right-bi.left;ep=gap*1e-5
 ll=[bi.mat(bi.left+e)[1]/e for e in [ep,ep/2]]
 rr=[-bi.mat(bi.right-e)[1]/e for e in [ep,ep/2]]
 return 2*ll[1]-ll[0],2*rr[1]-rr[0]
def endpoint_seed(mm,side,word,ain,krow):
 # Return logseedmatrix, list strictlinearconditions, outgoingpolya.
 m=mm[side+'growth'].shape[0];Z=np.eye(m);W=np.zeros(m);conditions=[];a=ain.copy();D=mm[side+'growth'];refs=mm[side+'reflect']
 for j in word:
  g=D@a;k=float(krow@a)
  if g[j]<=0:return None
  tau=Z[j].copy()/g[j];conditions.append(tau.copy())
  if k>0:conditions.append(W/k-tau)
  for l in range(m):
   if l!=j and g[l]>0:conditions.append(Z[l]/g[l]-tau)
  W-=k*tau;Z-=g[:,None]*tau;Z[j]=0
  a=refs[j]@a
 g=D@a;k=float(krow@a)
 if k<=0:return None
 tau=W/k;conditions.append(tau.copy())
 for j in range(m):
  if g[j]>0:conditions.append(Z[j]/g[j]-tau)
 Z-=g[:,None]*tau
 conditions.extend(list(Z.copy()))
 return Z,np.array(conditions),a

def seed_cycle(mm,bi,a,wordL,wordR,klkr=None):
 U=mm['U'];kl,kr=kappa_rows(bi) if klkr is None else klkr;ar=U@a
 r=endpoint_seed(mm,'R',wordR,ar,kr)
 if r is None:return []
 SR,cr,aoutR=r;ainL=np.linalg.solve(U,aoutR)
 l=endpoint_seed(mm,'L',wordL,ainL,kl)
 if l is None:return []
 SL,cl,aoutL=l;S=SL@SR;C=np.vstack([cr,cl@SR]);vals,vecs=np.linalg.eig(S);ans=[]
 for i,lam in enumerate(vals):
  if abs(lam.imag)>1e-6 or lam.real<=1.00001:continue
  for sign in [1,-1]:
   z=sign*vecs[:,i].real;z/=np.linalg.norm(z)
   margins=C@z
   if np.min(z)>1e-7 and np.min(margins)>1e-8:
    ans.append(dict(S=S,z=z,lam=lam.real,C=C,margin=np.min(margins),SR=SR,SL=SL))
 return ans
