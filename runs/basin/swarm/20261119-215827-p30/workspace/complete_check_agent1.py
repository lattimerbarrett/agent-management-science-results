from math import comb
import sympy as S

def matrices(k):
    n=2*k+2
    re=[S.zeros(n) for _ in range(2*k+1)]
    im=[S.zeros(n) for _ in range(2*k+1)]
    for a in range(k+1):
        for b in range(k+1):
            re[a+b][a,b]+=1
            re[a+b][k+1+a,k+1+b]-=1
            im[a+b][a,k+1+b]+=1
            im[a+b][k+1+b,a]+=1
    re[0]-=S.eye(n)
    re[-1]-=S.eye(n)
    F=re+im
    H=-re[0]-re[-1]
    A=[3*H+f for f in F]
    return F,H,A

def check(k):
    F,H,A=matrices(k); n=2*k+2; j=4*k+2
    assert len(F)==j and all(f==f.T for f in F)
    assert H.is_diagonal() and min(H.diagonal())>=1
    for a in A:  # rational, strict diagonal dominance proves positive definite
        assert all(a[r,r]>sum(abs(a[r,c]) for c in range(n) if c!=r) for r in range(n))
    # A=TF, det(T)=-5: invertible replacement of the output forms.
    h=S.zeros(1,j);h[0,0]=h[0,2*k]=-1
    T=S.eye(j)+3*S.ones(j,1)*h
    assert T.det()==-5
    # Check coefficient formulas symbolically with independent p,q.
    if k<=3:
        x=S.symbols('x:'+str(n)); y=S.symbols('y:'+str(n)); z=S.Symbol('z')
        p=sum((x[a]+S.I*x[k+1+a])*z**a for a in range(k+1))
        q=sum((y[a]+S.I*y[k+1+a])*z**a for a in range(k+1))
        t=sum(x[a]*y[a] for a in range(n))
        out=S.Poly(S.expand(p*q-t*(1+z**(2*k))),z)
        xv,yv=S.Matrix(x),S.Matrix(y)
        for ell in range(2*k+1):
            actual=(xv.T*F[ell]*yv)[0]+S.I*(xv.T*F[2*k+1+ell]*yv)[0]
            assert S.expand(actual-out.nth(ell))==0
    return n,j

for s in range(3,7):
    n=2**(s-1); j=2*n-2; d=3*n-2; k=(n-2)//2
    assert comb(j,n)%2==1
    # Expand and truncate the Stiefel-Whitney polynomial exactly mod 2.
    support=[(j+r,2*j-r) for r in range(j+1)
             if comb(j,r)%2 and j+r<=d and 2*j-r<=d]
    assert (d,d-2) in support
    assert check(k)==(n,j)
    print('s=',s,'D=',d,'matrix size=',n,'Euler support=',support)

# Verify all coefficient identities for a third, non-Mersenne parameter too.
check(2)
print('All exact checks passed.')

