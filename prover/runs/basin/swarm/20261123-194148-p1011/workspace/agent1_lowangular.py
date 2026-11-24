import numpy as np
from scipy.special import gammaln
from math import comb

def Cmat(n,ell,d,N=30000):
 a=(n+2*ell-3)/2; alpha=a+.5; j=np.arange(max(0,2-ell),N,dtype=float); k=j+ell
 base=max(1,ell)
 logI=gammaln(j+base)-gammaln(j+1)+gammaln(j+2*a+1)-gammaln(j+2*a-base+2)
 logh=gammaln(j+2*alpha)-gammaln(j+1)-np.log(j+alpha)
 logb=np.log(2)+gammaln((k+n+1)/2)+gammaln(k/2)-gammaln((k+n)/2)-gammaln((k-1)/2)
 lw=2*logI-logh-logb; w=np.exp(lw-lw.max())
 ratios={base:np.ones_like(j)}
 for p in range(base,ell+d): ratios[p+1]=ratios[p]*(j+p)*(2*a-p+1+j)/(p*2*(a-p))
 if ell==0: ratios[0]=np.zeros_like(j)
 gs=[]
 start=max(0,2-ell)
 for q in range(start,d+1):
  c=q*(2*q+n+2*ell-3)/(n-1); vec=np.zeros_like(j)
  for e,coef in [(q-1,c),(q,c+1-ell-2*q)]:
   if e<0 or coef==0:continue
   for p in range(e+1):vec+=coef*comb(e,p)*2**p*(-1)**(e-p)*ratios[ell+p]
  gs.append(vec)
 C=(np.array(gs)*w)@np.array(gs).T
 scale=np.sqrt(np.diag(C)); C=C/scale[:,None]/scale[None,:]
 ids=np.arange(start,d+1); D=(ell-1+ids[:,None]+ids[None,:])*C
 return np.linalg.eigvalsh(D)
for ell in [0,1]:
 for d in range(max(0,2-ell)+1,7):
  first=None
  for n in range(max(3,2*ell+4*d+1),60):
   ev=Cmat(n,ell,d)
   if ev[0]<-1e-6:first=n;break
  print(ell,d,first)
import pathlib
