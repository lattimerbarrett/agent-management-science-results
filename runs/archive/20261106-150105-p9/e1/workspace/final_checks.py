import math
import numpy as np
import sympy as S
from scipy.special import roots_jacobi

# Exact upper-exponent, reverse-Holder, and lower-parameter identities.
p,z,t,x,y=S.symbols('p z t x y', positive=True)
q=p/(p-1)
L=S.log(4)-x/p-y/q
d=S.log(2)/L
alpha=1-d+x/L; beta=1-d+y/L
assert S.simplify(alpha/p+beta/q-d)==0
assert S.simplify((1-d-alpha)*L+x)==0
assert S.simplify((1-d-beta)*L+y)==0
assert S.simplify(1/p+1/(p*(p-1))+1/q-(1+1/(p-1)-1/p))==0
aH=q*(1+z)/(q*(1+z)-1)
bH=p*(1+z)/(p*(1+z)-1)
assert S.simplify(p-aH-z*p*(p-1)/(1+p*z))==0
assert S.simplify(q-bH-z*p/((p-1)*(p+p*z-1)))==0
Z=1+t/4
assert S.simplify(1+(Z-1)/(1-(1-t)*Z)-(4+t)/(3+t))==0
print('7 exact symbolic identities: PASS')

# Exact, rational finite Hardy factorization and finite-plateau pairing.
a=S.Rational(4,5); b=S.Rational(9,10); N=12
La=S.Matrix(N,N,lambda i,j:a**(i-j) if i>=j else 0)
Ub=S.Matrix(N,N,lambda i,j:b**(j-i) if j>=i else 0)
C=La*Ub
for n in range(N):
    for m in range(N):
        assert C[n,m]==sum(a**(n-k)*b**(m-k) for k in range(min(n,m)+1))
assert sum(C)/N==sum((1-a**j)*(1-b**j) for j in range(1,N+1))/(N*(1-a)*(1-b))
print('144 exact Hardy entries and finite pairing: PASS')

# Integer enumeration: pair proportions and cross-level disjointness.
for n,m in [(3,4),(5,5),(6,4)]:
    used=set()
    for k in range(min(n,m)-1):
        pairs=set()
        for i in range(2**n):
            for j in range(2**m):
                if (i>>(n-k)) != (j>>(m-k)): continue
                u=(i>>(n-k-2))&3; v=(j>>(m-k-2))&3
                if (u,v) in [(0,3),(3,0)]: pairs.add((i,j))
        assert len(pairs)==2**(n+m-k-3)
        assert not used.intersection(pairs)
        used.update(pairs)
print('Exact Cantor pair counts and disjointness: PASS')

# Actual kernel quadrature, not the claimed asymptotic printed as evidence.
P=3.; Q=P/(P-1); rhoA=.96; rhoB=.92
r=.25*rhoA**(1/P)*rhoB**(1/Q)
logr=math.log(1/r); dim=math.log(2)/logr
al=1-dim+math.log(rhoA)/logr
be=1-dim+math.log(rhoB)/logr

def nodes(n,theta):
    z,w=roots_jacobi(12,-theta,-theta); w=w/w.sum()
    xx=[]; tt=[]; ww=[]
    for j in range(2**n):
        left=0.; val=0.
        for k in range(n):
            bit=(j>>(n-1-k))&1
            left+=bit*(1-r)*r**k; val+=bit*2.**(-k-1)
        lo=left+r**(n+1); hi=left+(1-r)*r**n
        xx.extend((lo+hi)/2+(hi-lo)*z/2)
        tt.extend([val+2.**(-n-1)]*len(z)); ww.extend(w/2**n)
    return np.array(xx),np.array(tt),np.array(ww)

ratios=[]
for n in range(2,6):
    X,T,U=nodes(n,al)
    for m in range(2,6):
        Y,V,Z=nodes(m,be)
        dx=X[:,None]-Y[None,:]; dt=T[:,None]-V[None,:]
        kernel=np.divide(dt,dx,out=np.zeros_like(dx),where=np.abs(dx)>1e-15)
        assert kernel.min()>-1e-11
        computed=float(U@kernel@Z)
        bound=sum((1/(4*r))**k for k in range(min(n,m)-1))/16
        assert computed>=bound-1e-10
        ratios.append(computed/bound)
print('16 independently integrated kernel blocks: PASS; minimum ratio =',min(ratios))
