import numpy as np
from scipy.special import gammaln
from math import comb
# Independent quadrature-free spectral sum for the angular-degree-2 block.
# Graphs P2(x') times polynomials of degree <=3 in |x'|^2.
for n in (18,19):
 k=np.arange(60000,dtype=float); b=(n+1)/2; L=k+2
 loga=2*np.log(L-1)+2*np.log(L+n-1)-np.log(2)+gammaln((L-1)/2)+gammaln((L+n)/2)-gammaln((L+n+1)/2)-gammaln(L/2)
 logI=2*b*np.log(2)+gammaln(b+k+1)+gammaln(b)-gammaln(2*b+k+1)
 logh=(2*b+1)*np.log(2)-np.log(2*k+2*b+1)+2*gammaln(k+b+1)-gammaln(k+1)-gammaln(k+2*b+1)
 wt=np.exp(loga+2*logI-logh)
 ratios=[np.ones_like(k)]
 for q in range(1,4): ratios.append(ratios[-1]*(k+q)/q*(2*b+k-q+1)/(b-q))
 R=np.array([sum((-1)**(j-q)*comb(j,q)*ratios[q] for q in range(j+1)) for j in range(4)])
 Q=(R*wt)@R.T
 M=np.array([[(1+i+j)*Q[i,j] for j in range(4)] for i in range(4)])
 diag=np.sqrt(np.diag(M)); norm=M/np.outer(diag,diag)
 print('n =',n,'normalized dilation-block eigenvalues:',np.linalg.eigvalsh(norm))
print('These are independent numerical checks only; the exact certificates previously run establish the signs.')
