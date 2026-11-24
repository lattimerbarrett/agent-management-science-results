import sympy as s
eta,t,d=s.symbols('eta t d', positive=True)
# If eta <= t*(1-d)+d, then d >= (eta-t)/(1-t).
threshold=s.factor((eta-t)/(1-t))
print('Dimension lower bound at t=eta/2:',s.simplify(threshold.subs(t,eta/2)))
print('Partial sum bound at t=eta/2:',s.simplify((1/t).subs(t,eta/2)))
# For a finite family p_i, V=[p_1 ... p_N],
# VV*=sum p_i. Its Gram matrix has the same nonzero spectrum.
import numpy as np
rng=np.random.default_rng(7)
P=[]
for i in range(5):
    v=rng.normal(size=(8,1))+1j*rng.normal(size=(8,1))
    v/=np.linalg.norm(v)
    P.append(v@v.conj().T)
V=np.concatenate(P,axis=1)
print('row/Gram norm agreement:',np.linalg.norm(V@V.conj().T,2),np.linalg.norm(V.conj().T@V,2))
