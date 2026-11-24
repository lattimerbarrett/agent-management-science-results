"""Hilbert-space two-small-red-rows lemma: exact and numerical checks."""
import sympy as s
import numpy as np

def checks():
    z=s.symbols('z',nonnegative=True)
    d=s.symbols('d',nonnegative=True)
    h=1-d-z*s.sqrt(1-2*d+z*z)
    assert s.expand((1-2*z+z*z)-(1-z)**2)==0
    endpoint=1-z-z*(1-z)  # sqrt((1-z)^2)=1-z since z<=1/2.
    assert s.expand(endpoint-(1-z)**2)==0
    assert s.simplify(s.diff(h,d)+1-z/s.sqrt(1-2*d+z*z))==0
    # For 0<=d<=z<=1/2, sqrt(1-2d+z²)>=z follows from 1-2d>=0.
    rho=s.symbols('rho')
    assert s.expand((z-rho)**2-(1-rho)*(z*z-rho)-rho*(1-z)**2)==0
    rng=np.random.default_rng(1931)
    for m in range(2,30):
        for _ in range(100):
            a=rng.uniform(.001,.25)
            w=rng.dirichlet(np.ones(m))
            f=rng.random(m)
            g=rng.random(m)
            f*=min(1,np.sqrt(a/np.dot(w,f*f)))
            g*=min(1,np.sqrt(a/np.dot(w,g*g)))
            lhs=np.dot(w,(1-f)*(1-g))
            assert lhs+1e-12>=(1-np.sqrt(a))**2
    print('Two-small-red-rows lemma checked exactly and on 2800 weighted pairs.')

if __name__=='__main__':
    checks()
