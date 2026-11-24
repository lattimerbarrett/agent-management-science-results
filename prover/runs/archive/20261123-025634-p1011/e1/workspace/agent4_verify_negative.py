"""Numerically falsifies one candidate weighted-shape Hessian positivity lemma.
This is NOT a counterexample to boundary Yamabe compactness.
Requires agent4_jet_matrix.py in the same directory.
"""
import numpy as np
from scipy.special import eval_jacobi, gamma
from scipy.integrate import quad
from math import comb
from agent4_jet_matrix import block
n=19;l=2;alpha=l+(n-3)/2
for j in range(4):
    for k in range(5):
        exact=quad(lambda z:(1-z)**(alpha+j)*(1+z)**(alpha+1-l-j)*eval_jacobi(k,alpha,alpha,z),-1,1,epsabs=1e-11,epsrel=1e-11)[0]
        val=0.
        for h in range(j+1):
            beta=1-l-j+h
            moment=(-1)**k*2**(2*alpha+beta+1)*gamma(alpha+k+1)*gamma(alpha+beta+1)*gamma(k-beta)/(gamma(-beta)*gamma(k+1)*gamma(2*alpha+beta+k+2))
            val+=comb(j,h)*2**(j-h)*(-1)**h*moment
        assert abs(val-exact)<1e-8*max(1,abs(exact)),(j,k,val,exact)
print('20 quadrature moment checks passed')
last=None
for K in [100,1000,10000,100000]:
    js,eigenvalues,B=block(19,2,K)
    print('cutoff',K,'degrees',[l+2*j for j in js],'eigenvalues',eigenvalues)
    last=eigenvalues
assert last[0]<-0.0011
print('Numerical evidence only: weighted Hessian has negative direction. No rigorous series-tail bound computed.')
