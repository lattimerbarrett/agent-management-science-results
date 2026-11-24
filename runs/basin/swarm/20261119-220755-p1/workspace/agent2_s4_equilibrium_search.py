import numpy as np
from scipy.optimize import brentq
from itertools import combinations
from pathlib import Path
s=4
base=np.array([-3.,-1.,0.,1.,2.,3.]); fcoef=np.array([63/40,0.,-9/2,0.]);gcoef=np.array([187/40,0.,-19/2,0.]);N=11781/1600
P=np.poly(base);ds=np.polyval(np.polyder(P),base)
f=lambda z:z**4+sum(fcoef[j]*z**j for j in range(4));g=lambda z:z**4+sum(gcoef[j]*z**j for j in range(4))
neg=np.roots(np.polymul(np.r_[1,fcoef[::-1]],np.r_[1,gcoef[::-1]])+np.r_[np.zeros(8),N]);neg=np.sort(neg.real[abs(neg.imag)<1e-8]);print('negative modes',neg)
V=np.array([base**j for j in range(4)]).T

def data(theta,mus):
 H=base-theta;p=N*H/(ds*f(base));pp=H*f(base)/ds;M=V.T@(p[:,None]*V);Mp=V.T@(pp[:,None]*V)
 force=np.linalg.solve(M,np.array([4*f(mu)*np.array([mu**j for j in range(4)]) for mu in mus]).T)
 K=[];L=[]
 for k in range(4):
  uv=base**k;delta_pp=H*uv/ds;dg=np.linalg.solve(Mp,-V.T@(delta_pp*g(base)))
  dN=N*N*np.sum(H*uv/(ds*f(base)**2))
  # remainder H*(u*g+f*dg), represented descending coefficients.
  up=np.zeros(4);up[k]=1
  dproduct=np.polyadd(np.polymul(np.r_[0,up[::-1]],np.r_[1,gcoef[::-1]]),np.polymul(np.r_[1,fcoef[::-1]],np.r_[0,dg[::-1]]))
  rem=np.polydiv(np.polymul([1,-theta],dproduct),P)[1]; rem=np.pad(rem,(max(0,2-len(rem)),0))
  dNp=rem[-2] if len(rem)>1 else 0;dtheta=(-rem[-1]-theta*dNp)/N
  K.append(dtheta)
  L.append([2*(mu**k/f(mu)+sum(dg[j]*mu**j for j in range(4))/g(mu))-2*dN/N for mu in mus])
 L=np.array(L).T;K=np.array(K)
 Z=np.linalg.solve(L@force,np.array([-2.,-2.]))
 return K@force@Z,Z,force@Z
allroots=np.sort(np.roots(np.polymul(np.r_[1,fcoef[::-1]],np.r_[1,gcoef[::-1]])).real)
found=[]
for ix in combinations(range(8),4):
 if 0 not in ix:continue
 fcoef=np.poly(allroots[list(ix)])[1:][::-1];gcoef=np.poly(allroots[[i for i in range(8) if i not in ix]])[1:][::-1]
 signs=ds*f(base)
 lo=max(base[signs<0],default=-np.inf);hi=min(base[signs>0],default=np.inf)
 if not lo<hi or not np.isfinite(lo+hi):continue
 for mus in combinations(neg,2):
  vals=[]
  for th in np.linspace(lo+(hi-lo)*.001,hi-(hi-lo)*.001,51):
   try:vals.append((th,*data(th,mus)))
   except np.linalg.LinAlgError:pass
  for aa,bb in zip(vals[:-1],vals[1:]):
   if aa[1]*bb[1]<0:
    th=brentq(lambda t:data(t,mus)[0],aa[0],bb[0]);v,Z,u=data(th,mus)
    if min(Z)>0:
     item=(ix,lo,hi,mus,th,Z.tolist(),u.tolist());found.append(item);print('POSITIVE',item)
print('TOTAL POSITIVE',len(found))
Path('workspace/agent2_s4_equilibrium_search.py').write_text(Path('scratchpad.py').read_text())
