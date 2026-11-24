from pathlib import Path
import sympy as s
import numpy as np
# Levi normal-direction correction: H + 2*C dr \otimes dr.
l,a,b1,b2,d,C=s.symbols('lambda a b1 b2 d C',real=True)
i=s.I
H=s.Matrix([[l,b1+i*b2],[b1-i*b2,d+2*C*a*a]])
assert s.expand(H.det()-(l*(d+2*C*a*a)-b1*b1-b2*b2))==0
# Choose the bottom-right entry = (|b|^2/lambda)+t.
t=s.symbols('t',positive=True)
Ht=H.subs(d,b1*b1/l+b2*b2/l+t-2*C*a*a)
assert s.simplify(Ht.det()-l*t)==0
# Test representative normalized Levi forms, including large mixed terms.
rng=np.random.default_rng(20260609)
min_eval=float('inf')
for _ in range(10000):
    lam=float(np.exp(rng.uniform(-4,4))); aa=float(np.exp(rng.uniform(-4,4)))
    bb=complex(*rng.normal(size=2)); dd=float(rng.normal()*20)
    cc=(abs(bb)**2/lam+abs(dd)+lam)/(2*aa**2)
    mat=np.array([[lam,bb],[bb.conjugate(),dd+2*cc*aa**2]],complex)
    ev=np.linalg.eigvalsh(mat)
    assert ev[0]>0
    min_eval=min(min_eval,float(ev[0]))
# Radius/gluing inequalities are exact rational comparisons.
eps=s.Rational(1,7); R=s.Rational(1,3)
cut=-eps*R**2/2
assert -eps*R**2<cut<0
print('Symbolic determinant and Schur-complement identities verified.')
print('10000 sampled Hermitian normal corrections positive definite; min eigenvalue:',min_eval)
print('Exact gluing inequality:',-eps*R**2,'<',cut,'< 0')
