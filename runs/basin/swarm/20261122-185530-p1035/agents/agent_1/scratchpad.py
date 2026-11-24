from math import comb, factorial
from fractions import Fraction as F
from itertools import product
import sympy as S
import numpy as np

def C(n,k):
    return comb(n,k) if n>=k>=0 else 0

def baseline(m,s,q):
    return 1+3*m*q**(m+1)*C(s+m-1,m+1)+F(3*m,2)*q**m*(q-1)*C(s+m-1,m)

def length_formula(m,s,q):
    h=s*q//(3*s-1)
    return baseline(m,s,q)+C(s+m-1,m-1)*(3*s*q*C(h+m,m)-3*s-3*m*(3*s-1)*C(h+m,m+1))

def poly_value(m,s,q):
    h=(q-1)//3
    return baseline(m,s,q)+C(s+m-1,m-1)*(3*s*q*C(h+m,m)-3*s-3*m*(3*s-1)*C(h+m,m+1))

def discrepancy(m,s):
    return F(C(s+m-1,m-1),factorial(m+1))*(F(3*s**(m+1),(3*s-1)**m)-F(3*s+m,3**m))

# Direct basis computations in A = F_7[x,y,z]/(z^3+x^3+y^3).
def basis(d):
    return [(i,d-i-j,j) for j in range(min(2,d)+1) for i in range(d-j+1)]

def reduce_monomial(a,b,c):
    h,j=divmod(c,3)
    out={}
    for v in range(h+1):
        key=(a+3*v,b+3*(h-v),j)
        out[key]=((-1)**h*comb(h,v))%7
    return out

def rank_mod7(mat):
    a=np.array(mat,dtype=np.int64)%7
    nr,nc=a.shape
    row=0
    for col in range(nc):
        idx=np.flatnonzero(a[row:,col])
        if len(idx)==0: continue
        j=row+int(idx[0])
        a[[row,j]]=a[[j,row]]
        a[row]=(a[row]*pow(int(a[row,col]),-1,7))%7
        targets=np.flatnonzero(a[:,col]); targets=targets[targets!=row]
        a[targets]=(a[targets]-a[targets,col,None]*a[row])%7
        row+=1
        if row==nr: break
    return row

def a_rank(s,r,q):
    dest=basis(s*q+r); index={v:i for i,v in enumerate(dest)}
    cols=[]
    for v in basis(s):
        for w in basis(r):
            exp=tuple(q*v[i]+w[i] for i in range(3))
            col=[0]*len(dest)
            for key,c in reduce_monomial(*exp).items(): col[index[key]]=c
            cols.append(col)
    return rank_mod7(np.array(cols).T)

checks=0
for q in [1,7]:
    for s in range(1,5):
        for r in range(q+1):
            rank=a_rank(s,r,q)
            defect=3*s*(q-1) if r==0 else max(3*s*q-3*(3*s-1)*r,0)
            assert rank==3*(s*q+r)-defect,(s,r,q,rank,defect)
            checks+=1
print('Direct Frobenius multiplication ranks in A checked:',checks)

# Independent monomial enumeration in B and rank computation in A,
# summed degree-by-degree (not the closed length formula).
checks=0
for q in [1,7]:
    for s in range(1,4):
        aranks={r:a_rank(s,r,q) for r in range(q)}
        for m in range(2,5):
            maxdeg=max(s*q+q,(s-1)*q+m*(q-1))+1
            bquot=[0]*(maxdeg+1)
            # floor-vector multiplicities and each residual monomial
            for j in range(s):
                for residual in product(range(q),repeat=m):
                    bquot[q*j+sum(residual)]+=C(j+m-1,m-1)
            value=0
            for t in range(maxdeg+1):
                adim=1 if t==0 else 3*t
                bdim=C(t+m-1,m-1)
                brank=bdim-bquot[t]
                if brank==0: arank=0
                elif t-s*q<q: arank=aranks[t-s*q]
                else: arank=adim # confirmed vanish-range by slope lemma
                value+=adim*bdim-arank*brank
            assert value==length_formula(m,s,q),(m,s,q,value,length_formula(m,s,q))
            checks+=1
print('Independent degreewise length checks:',checks)

# Symbolic identities: closed summations, asymptotic polynomial and limit.
x,u=S.symbols('x u',positive=True)
for m in range(2,13):
    cs=S.prod(x+j for j in range(1,m))/factorial(m-1)
    integrand=3*(x-(3*x-1)*u)*u**(m-1)/factorial(m-1)
    R=cs*S.integrate(integrand,(u,0,x/(3*x-1)))
    R0=cs*S.integrate(integrand,(u,0,S.Rational(1,3)))
    assert S.simplify(R-3*cs*x**(m+1)/(factorial(m+1)*(3*x-1)**m))==0
    assert S.simplify(R0-cs*(3*x+m)/(3**m*factorial(m+1)))==0
    for s in range(1,8):
        for q in [1,7,49,343]:
            h=s*q//(3*s-1)
            direct=baseline(m,s,q)+C(s+m-1,m-1)*(3*s*(q-1)+sum((3*s*q-3*(3*s-1)*r)*C(r+m-1,m-1) for r in range(1,h+1)))
            assert direct==length_formula(m,s,q)
        # Eventual equality to the exact Hilbert polynomial.
        for q in [1,7,49]:
            for z in range(q+2,q+7):
                assert length_formula(m,z,q)==poly_value(m,z,q)
        # Genuine numerical convergence against the claimed limiting discrepancy.
        q=7**9
        actual=(length_formula(m,s,q)-poly_value(m,s,q))/q**(m+1)
        expected=discrepancy(m,s)
        assert abs(actual-expected)<F(1,100000)*max(F(1),abs(expected)),(m,s,float(actual),float(expected))
print('Symbolic integral identities, exact sums, eventual polynomial, convergence: passed')
print('Sample limiting discrepancies for (m,s)=(2,1),(2,2),(3,1),(4,3):')
for m,s in [(2,1),(2,2),(3,1),(4,3)]: print((m,s),discrepancy(m,s))
