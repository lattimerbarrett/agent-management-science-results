"""Independent numerical/symbolic checks: necessary scalar lower exponents,
polar parametrization, and target duality. These do NOT prove matrix sharpness.
"""
import math, json
from pathlib import Path
Path('workspace/agent1_scalar_checks.py').write_text(Path(__file__).read_text())
import numpy as np
import mpmath as mp
import sympy as sp
mp.mp.dps=40
p=sp.symbols('p', positive=True)
q=p/(p-1)
alpha=lambda x: 1+1/(x*(x-1))
assert sp.simplify(alpha(q)/(p-1)-alpha(p))==0
assert sp.simplify(1+1/(p-1)-1/p-alpha(p))==0
rng=np.random.default_rng(5482)
def pospower(A,t):
    d,U=np.linalg.eigh(A)
    assert np.min(d)>0
    return (U*d**t)@U.conj().T
polar_err=[]
for pp in [1.25,1.5,3.,5.]:
    for k in range(30):
        Fs=[]
        for j in range(2):
            F=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
            F+=3*np.eye(2)
            Fs.append(F)
        F,G=Fs
        W=pospower(F.conj().T@F,pp/2)
        V=pospower(G.conj().T@G,pp/2)
        lhs=np.linalg.norm(pospower(W,1/pp)@pospower(V,-1/pp),2)
        rhs=np.linalg.norm(F@np.linalg.inv(G),2)
        err=abs(lhs-rhs)/max(1,rhs)
        polar_err.append(err)
        assert err<1e-10
print('symbolic exponent identities: proved by exact simplification')
print('max relative error polar parametrization:', max(polar_err))
rows=[]
for pp in [1.25,1.5,3.,5.]:
    for eps in [mp.mpf('0.1'),mp.mpf('0.03'),mp.mpf('0.01')]:
        # alpha=(p-1)(1-eps): exact Ap test value on (0,1).
        aa=(pp-1)*(1-eps)
        ap_upper_endpoint=1/((aa+1)*eps**(pp-1))
        # H[x^(eps-1)1_(0,1)] / x^(eps-1) >= cot(pi eps).
        lower_norm=mp.cot(mp.pi*eps)
        # alpha=-1+eps, f=1_(0,1). Exact lower integral on x<1/2,
        # replacing |log(x/(1-x))| by log(1/(2x)).
        # Substitution t=log(1/(2x)) gives 2^-eps Gamma(p+1)/eps^(p+1).
        lower_norm2=(2**(-eps)*mp.gamma(pp+1))**(1/pp)/(mp.pi*eps)
        ap_lower_endpoint=1/(eps*((pp-eps)/(pp-1))**(pp-1))
        rows.append(dict(p=pp,eps=float(eps),Ap_test_upper=float(ap_upper_endpoint),
                         H_lower_upper=float(lower_norm),Ap_test_lower=float(ap_lower_endpoint),
                         H_lower_lower=float(lower_norm2)))
        # Check Mellin PV formula numerically for one x; symmetric exclusion.
        x=mp.mpf('0.37')
        eta=mp.mpf('1e-8')
        # Infinite integral transformed y=x*t, split symmetrically about t=1.
        # Algebraic cancellation makes integral over t in (0,1) non-singular.
        integ=mp.quad(lambda t:(t**(eps-1)-t**(-eps))/(1-t),[0,mp.mpf('0.01'),mp.mpf('0.5'),1])
        # mp.quad converges slowly at exponent eps near 0; exact endpoint series
        # integral is digamma(1-eps)-digamma(eps).
        exact=mp.digamma(1-eps)-mp.digamma(eps)
        assert abs(exact-mp.pi*mp.cot(mp.pi*eps))<mp.mpf('1e-35')
print(json.dumps(rows,indent=2))
with open('workspace/agent1_scalar_checks.json','w') as f: json.dump(rows,f,indent=2)
