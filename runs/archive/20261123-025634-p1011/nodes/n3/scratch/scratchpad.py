import numpy as np
import math
from scipy.special import gammaln, poch, comb
for n in range(5,41):
 S=(n-5)//4
 if S<1: continue
 j=np.arange(0.,30000.)
 k=j+2
 logq=2*np.log(k-1)+2*np.log(k+n-1)+gammaln((k-1)/2)+gammaln((k+n)/2)-np.log(2)-gammaln(k/2)-gammaln((k+n+1)/2)
 lw=logq+gammaln(j+1)+np.log(j+(n+2)/2)-gammaln(j+n+2)
 w=np.exp(lw-lw[0])
 R=[]
 for s in range(S+1):
  r=np.zeros_like(j)
  for t in range(s+1):
   r+=(-1)**(s-t)*comb(s,t)*poch(j+1,t)*poch(j+n+2-t,t)/(math.factorial(t)*poch((n+1)/2-t,t))
  R.append(r)
 R=np.array(R)
 A=(R*w)@R.T
 sc=np.sqrt(np.diag(A)); A=A/sc[:,None]/sc[None,:]
 inds=np.arange(S+1)
 B=A*(1+inds[:,None]+inds[None,:])
 e=np.linalg.eigvalsh(B)
 print(n,S,e[0])
