"""Exact construction and checks of the sharp Gaussian lower bound.
All arithmetic is integer. No numerical root finding is used.
Run: python agent2_gaussian_lower.py
"""
from itertools import combinations
from math import comb

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c

def factor(roots):
    p=[1]
    for r in roots:p=mul(p,[r,1])
    return p

def data(s):
    assert s>=3
    n=2**(s-1);k=n//2
    P=factor(range(1,2*k-1));C=max(P);T=2*C*C+2
    J=[[0]*k for _ in range(k)];power=1
    for a in range(k):
        for b in range(a+1,k):
            J[a][b]=power;J[b][a]=-power;power*=T
    return n,k,P,C,T,J

def pair(x,y,D):
    n,k,P,C,T,J=D
    a,b=x[:k],x[k:];c,d=y[:k],y[k:]
    ac,bd,ad,bc=mul(a,c),mul(b,d),mul(a,d),mul(b,c)
    real=[u-v for u,v in zip(ac,bd)]
    imag=[u+v for u,v in zip(ad,bc)]
    real=[real[i]-real[-1]*P[i] for i in range(2*k-2)]
    imag=[imag[i]-imag[-1]*P[i] for i in range(2*k-2)]
    norm=sum(xi*yi for xi,yi in zip(x,y))
    skew=sum(J[i][j]*(-a[i]*d[j]+b[i]*c[j]) for i in range(k) for j in range(k))
    return real+imag+[norm,skew]

def matrices(D):
    n,k,P,C,T,J=D;m=2*n-2
    basis=[[int(i==j) for i in range(n)] for j in range(n)]
    H=[[[0]*n for _ in range(n)] for _ in range(m)]
    for i in range(n):
        for j in range(n):
            vals=pair(basis[i],basis[j],D)
            assert len(vals)==m
            for l,v in enumerate(vals):H[l][i][j]=v
    assert all(H[l][i][j]==H[l][j][i] for l in range(m) for i in range(n) for j in range(n))
    norm_index=m-2
    assert H[norm_index]==basis
    R=1+max(sum(abs(v) for v in row) for M in H for row in M)
    # The covariance forms are I and R I+H_l for l != norm_index.
    # Their span equals span(H), and strict diagonal dominance proves PD.
    for l,M in enumerate(H):
        if l==norm_index:continue
        for i,row in enumerate(M):
            assert R+row[i] > sum(abs(row[j]) for j in range(n) if j!=i)
    return H,R

def check(s,exhaustive=True):
    D=data(s);n,k,P,C,T,J=D
    H,R=matrices(D)
    count=0
    if exhaustive:
        roots=set(range(1,2*k-1))
        for S in combinations(sorted(roots),k-1):
            U=factor(S);V=factor(sorted(roots-set(S)))
            assert mul(U,V)==P
            assert max(U)<=C and max(V)<=C
            h=sum(x*y for x,y in zip(U,V));assert h>0
            coeff=[U[a]*V[b]-U[b]*V[a] for a in range(k) for b in range(a+1,k)]
            assert any(coeff) # complementary monic factors are distinct
            assert max(map(abs,coeff))<=2*C*C
            value=sum(U[a]*J[a][b]*V[b] for a in range(k) for b in range(k))
            assert value==sum(c*T**e for e,c in enumerate(coeff))
            assert value!=0
            # Exact dominance certificate: nonzero leading coefficient wins.
            degree=max(i for i,c in enumerate(coeff) if c)
            assert abs(coeff[degree])*T**degree > sum(abs(coeff[i])*T**i for i in range(degree))
            count+=1
        assert count==comb(2*k-2,k-1)
    return {'s':s,'n':n,'number_measures':2*n-2,'counterexample_dimension':3*n-3,
            'forms_checked':len(H),'complementary_factorizations_checked':count,
            'largest_shift_bit_length':R.bit_length()}

if __name__=='__main__':
    for s in (3,4,5):print(check(s),flush=True)
