import numpy as np
import sympy as sp
from pathlib import Path

# Exact symbolic identities used by the upper-bound proof.
p=sp.symbols('p', positive=True)
q=p/(p-1)
d=sp.symbols('d', positive=True)
beta=1+1/(p*(p-1))
assert sp.simplify(1/p + 1/q + 1/(p*(p-1))-beta)==0
rf=q*(1+d)/(q*(1+d)-1)
assert sp.simplify(1/rf-1/p-d/(q*(1+d)))==0
assert sp.simplify(p-rf-p*(p-1)*d/(1+p*d))==0
assert sp.simplify((1+1/(q*(q-1)))/(p-1)-beta)==0
print('PASS: four exact symbolic upper-bound/duality identities')

rng=np.random.default_rng(20261004)
worst_primal=0.; worst_dual=0.; worst_mixed=0.
for exponent in [1.15,1.4,1.8,2.3,3.,5.,9.]:
    conjugate=exponent/(exponent-1)
    for trial in range(70):
        n=6
        prob=rng.dirichlet(np.ones(n))
        angles=rng.uniform(0,2*np.pi,n)
        eig=np.exp(rng.uniform(-4,4,(n,2)))
        roots=[]
        for angle,ev in zip(angles,eig):
            U=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
            roots.append((U*ev)@U.T)
        roots=np.array(roots)
        inv=np.linalg.inv(roots)
        K=np.array([[np.linalg.norm(roots[i]@inv[j],2) for j in range(n)] for i in range(n)])
        Q=np.dot(prob,(K**conjugate@prob)**(exponent/conjugate))
        Qdual=np.dot(prob,(K.T**exponent@prob)**(conjugate/exponent))
        worst_mixed=max(worst_mixed,Qdual**(1/conjugate)/Q**(1/exponent))
        for a in np.linspace(0,np.pi,73):
            e=np.array([np.cos(a),np.sin(a)])
            w=np.linalg.norm(roots@e,axis=1)**exponent
            u=np.linalg.norm(inv@e,axis=1)**conjugate
            scalar=np.dot(prob,w)*np.dot(prob,w**(-1/(exponent-1)))**(exponent-1)
            dual=np.dot(prob,u)*np.dot(prob,u**(-1/(conjugate-1)))**(conjugate-1)
            worst_primal=max(worst_primal,scalar/Q)
            worst_dual=max(worst_dual,dual**(1/conjugate)/Q**(1/exponent))
            assert scalar <= Q*(1+1e-8)
            # A dimension-only coarse bound, justified by reducing ellipsoids.
            assert dual**(1/conjugate) <= 16*Q**(1/exponent)*(1+1e-8)
print('PASS: 35,770 directional discrete tests of scalarization inequalities')
print('Maximum primal scalar Ap / matrix Ap:',worst_primal)
print('Maximum dual scalar characteristic root / matrix characteristic root:',worst_dual)
print('Maximum dual mixed-norm root / primal mixed-norm root:',worst_mixed)
