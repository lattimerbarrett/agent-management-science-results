import sympy as s
import numpy as np
p=s.symbols('p', positive=True)
q=p/(p-1)
beta=lambda t: 1+1/(t*(t-1))
assert s.simplify(beta(q)/(p-1)-beta(p))==0
assert s.simplify((s.Rational(3,2)-s.Rational(1,2)*(2-p))/(p-1)-beta(p)) != 0  # naive linear extrapolation not target
rng=np.random.default_rng(181)
def power(A,t):
    w,V=np.linalg.eigh(A)
    return (V*w**t)@V.conj().T

def ap_discrete(W,p):
    q=p/(p-1)
    A=np.array([power(w,1/p) for w in W])
    B=np.array([power(w,-1/p) for w in W])
    K=np.array([[np.linalg.norm(a@b,2) for b in B] for a in A])
    original=np.mean(np.mean(K**q,axis=1)**(p-1))
    dual=np.mean(np.mean(K.T**p,axis=1)**(q-1))
    return original,dual
worst=1.
for p0 in [1.1,1.25,1.5,1.9,2.,2.5,3.,5.,10.]:
    q0=p0/(p0-1)
    for trial in range(20):
        W=[]
        for j in range(7):
            Z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
            Q,_=np.linalg.qr(Z)
            W.append((Q*np.exp(rng.uniform(-4,4,2)))@Q.conj().T)
        W=np.array(W)
        # Dual kernel is exactly the transpose; avoid numerically ill-conditioned U.
        aa,bb=ap_discrete(W,p0)
        a=aa**(1/p0)
        b=bb**(1/q0)
        assert max(a/b,b/a)<=16*(1+1e-7)
        worst=max(worst,a/b,b/a)
print('Symbolic beta duality identity verified.')
print('180 finite-support noncommuting examples checked; maximum root ratio:',worst)
print('These numerical tests do not prove the analytic inequalities; the reducing-norm proof does.')
