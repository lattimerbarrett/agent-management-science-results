import numpy as np
from scipy.special import gammaln

def Q(n,N=20000,deg=2,ell=2):
 a=ell+(n-2)/2
 k=np.arange(N,dtype=float)
 # suppress constant same all entries in I and h
 Is=[]
 for p in range(ell-1,ell-1+deg):
  logI=(2*a-p)*np.log(2)+gammaln(a+.5-p)+gammaln(a+.5)-gammaln(2*a+1-p)
  logI+=gammaln(2*a+k)-gammaln(2*a)-gammaln(k+1)+gammaln(p+k)-gammaln(p)+gammaln(2*a+1-p)-gammaln(2*a+1-p+k)
  Is.append(np.exp(logI))
 import math
 F=[sum(math.comb(j,l)*2**l*(-1)**(j-l)*Is[l] for l in range(j+1)) for j in range(deg)]
 logh=np.log(np.pi)+(1-2*a)*np.log(2)+gammaln(k+2*a)-gammaln(k+1)-np.log(k+a)-2*gammaln(a)
 K=k+ell
 logt=np.log(2)+gammaln((K+n+1)/2)+gammaln(K/2)-gammaln((K-1)/2)-gammaln((K+n)/2)
 w=(K-1)**2*(K+n-1)**2*np.exp(-logt-logh)
 return np.array([[np.sum(w*f*g) for f in F] for g in F])
for n in range(7,30):
 out=[]
 for ell in range(2,(n-1)//2+1):
  deg=((n-1)//2-ell)//2+1
  q=Q(n, N=5000, deg=deg,ell=ell)
  q=q/np.sqrt(np.outer(np.diag(q),np.diag(q)))
  ids=np.arange(deg)+(ell-1)/2
  A=q*(ids[:,None]+ids[None,:])/np.sqrt(np.outer(2*ids,2*ids))
  vals=np.linalg.eigvalsh(A)
  out.append((vals[0],ell))
 print(n,min(out))
