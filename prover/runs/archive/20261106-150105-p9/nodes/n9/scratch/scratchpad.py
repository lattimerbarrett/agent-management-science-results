import numpy as np
from scipy.integrate import quad
from scipy.special import gamma

# w_epsilon(x)=|x|^(-1+epsilon), f=1_(0,1).
# The negative half-interval alone gives this exact norm-ratio lower bound.
# Its scalar Ap characteristic is comparable to epsilon^(-1).
for p in [1.5,3.0,4.0]:
    print('p =',p)
    for eps in [0.1,0.02,0.005]:
        J=quad(lambda u:(u+eps*np.log1p(np.exp(-u/eps)))**p*np.exp(-u),0,np.inf)[0]
        ratio=J**(1/p)/(np.pi*eps)
        print(' epsilon',eps,' epsilon * norm lower bound',eps*ratio)
    print(' limiting constant:',gamma(p+1)**(1/p)/np.pi)
    print(' scalar lower exponents: 1 and',1/(p-1))
    # Two-valued rotating-eigenvector weight.
    # Both matrices have eigenvalues t and 1; B=R A R^T.
    R=np.array([[1.,-1.],[1.,1.]])/np.sqrt(2)
    for t in [1e3,1e6]:
        Apow=np.diag([t**(1/p),1.])
        Bmin=R@np.diag([t**(-1/p),1.])@R.T
        M=np.linalg.norm(Apow@Bmin,2)
        q=p/(p-1)
        half_characteristic=((1+M**q)/2)**(p-1)
        # The input vector e2 has unit A-norm.
        Bpow=R@Apow@R.T
        amplification=np.linalg.norm(Bpow@np.array([0.,1.]))
        print(' t',t,' half-char/t',half_characteristic/t,
              ' cross amplification/t^(1/p)',amplification/t**(1/p))
