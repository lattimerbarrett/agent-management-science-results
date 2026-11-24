import numpy as np
from scipy.special import gammaln
from math import comb
for ell in range(2,9):
 for d in range(1,5):
  first=None
  for n in range(max(3,2*ell+4*d+1),50):
   a=(n+2*ell-3)/2; alpha=a+.5; js=np.arange(10000,dtype=float)
   logI=gammaln(js+ell)-gammaln(js+1)+gammaln(js+2*a+1)-gammaln(js+2*a-ell+2)
   logh=gammaln(js+2*alpha)-gammaln(js+1)-np.log(js+alpha)
   k=js+ell
   logb=np.log(2)+gammaln((k+n+1)/2)+gammaln(k/2)-gammaln((k+n)/2)-gammaln((k-1)/2)
   lw=2*logI-logh-logb; w=np.exp(lw-lw.max())
   ratios=[np.ones_like(js)]
   for p in range(ell,ell+d):
    ratios.append(ratios[-1]*(js+p)*(2*a-p+1+js)/(p*2*(a-p)))
   gs=[]
   for q in range(d+1):
    c=q*(2*q+n+2*ell-3)/(n-1); vec=np.zeros_like(js)
    for e,coef in [(q-1,c),(q,c+1-ell-2*q)]:
     if e<0: continue
     for p in range(e+1): vec+=coef*comb(e,p)*2**p*(-1)**(e-p)*ratios[p]
    gs.append(vec)
   C=(np.array(gs)*w)@np.array(gs).T
   scale=np.sqrt(np.diag(C)); C=C/scale[:,None]/scale[None,:]
   ij=np.arange(d+1)[:,None]+np.arange(d+1)[None,:]
   D=(2*ell-2+2*ij)*C
   ev=np.linalg.eigvalsh(D)
   if ev[0]<-1e-7: first=n; break
  print(ell,d,first)
