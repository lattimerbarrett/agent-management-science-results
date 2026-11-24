"""Exact Gaussian lower-bound certificates; no floating point arithmetic."""
from itertools import combinations
from fractions import Fraction

def polynomial(roots):
    p=[1]
    for r in roots:
        q=[0]*(len(p)+1)
        for i,a in enumerate(p): q[i]-=r*a; q[i+1]+=a
        p=q
    return p

def zero(n): return [[0]*n for _ in range(n)]
def eye(n): return [[int(i==k) for k in range(n)] for i in range(n)]
def certificate(s):
    assert s>=3
    n=2**(s-1); m=n//2; j=2*n-2
    roots=[2**r for r in range(2*m-2)]
    w=polynomial(roots)
    assert len(w)==2*m-1 and w[-1]==1
    I=eye(n)
    # Re <u,i K v>, supported on the two highest coefficients.
    K=zero(m); K[m-2][m-1]=1; K[m-1][m-2]=-1
    B=zero(n)
    for a in range(m):
        for b in range(m): B[a][m+b]=-K[a][b]; B[m+a][b]=K[a][b]
    forms=[I,B]
    # Complex product modulo Cw, eliminating its highest coefficient.
    for k in range(2*m-2):
        C=[[int(a+b==k)-w[k]*int(a+b==2*m-2) for b in range(m)] for a in range(m)]
        R=zero(n); T=zero(n)
        for a in range(m):
            for b in range(m):
                R[a][b]=C[a][b];R[m+a][m+b]=-C[a][b]
                T[a][m+b]=C[a][b];T[m+a][b]=C[a][b]
        forms.extend([R,T])
    assert len(forms)==j
    # Check every bilinear matrix entry against direct complex basis arithmetic.
    phase=[(1,0),(0,1),(-1,0),(0,-1)]
    for a in range(n):
        for b in range(n):
            ia,ib=a%m,b%m
            ea,eb=a//m,b//m
            expected=[int(a==b),phase[(1-ea+eb)%4][0]*K[ia][ib]]
            pr,pi=phase[(ea+eb)%4]
            for k in range(2*m-2):
                coeff=int(ia+ib==k)-w[k]*int(ia+ib==2*m-2)
                expected.extend([coeff*pr,coeff*pi])
            assert [B[a][b] for B in forms]==expected
    # Shift the forms other than I into the positive definite cone.
    covariances=[I]
    for B in forms[1:]:
        assert all(B[a][b]==B[b][a] for a in range(n) for b in range(n))
        shift=1+max(sum(abs(x) for x in row) for row in B)
        A=[[B[a][b]+shift*I[a][b] for b in range(n)] for a in range(n)]
        # Exact strict diagonal dominance, with positive diagonal, proves PD.
        assert all(A[a][a]>sum(abs(A[a][b]) for b in range(n) if b!=a) for a in range(n))
        assert [[A[a][b]-shift*I[a][b] for b in range(n)] for a in range(n)]==B
        covariances.append(A)
    checked=0
    for subset in combinations(range(2*m-2),m-1):
        subset=set(subset)
        p=polynomial([roots[a] for a in subset])
        q=polynomial([roots[a] for a in range(2*m-2) if a not in subset])
        product=[0]*(2*m-1)
        for a,pa in enumerate(p):
            for b,qb in enumerate(q): product[a+b]+=pa*qb
        assert product==w
        inner=sum(a*b for a,b in zip(p,q))
        wedge=p[-2]*q[-1]-p[-1]*q[-2]
        assert inner>0 and wedge!=0 and wedge%2==1
        assert wedge==sum((-roots[a] if a in subset else roots[a]) for a in range(2*m-2))
        checked+=1
    return {'s':s,'j':j,'bad_dimension':3*n-3,'normal_dimension':n,'SPD_matrices':len(covariances),'ordered_factorizations_checked':checked}

if __name__=='__main__':
    for s in (3,4,5): print(certificate(s),flush=True)
