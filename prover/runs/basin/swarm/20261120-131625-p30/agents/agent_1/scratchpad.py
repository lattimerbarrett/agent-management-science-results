from math import factorial, comb
from itertools import combinations
import sympy as S


def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c


def factor_vector(roots):
    a=[1]
    for r in roots: a=mul(a,[r,1])
    return a


def check(s, exhaustive=True):
    assert s>=3
    m=2**(s-2); n=2*m; j=4*m-2
    d0=6*m-3; d=d0+1
    roots=tuple(range(1,2*m-1))
    p=factor_vector(roots)
    C=factorial(2*m-1); T=4*C*C+2
    K=S.zeros(m); e=0
    for a in range(m):
        for b in range(a+1,m):
            K[a,b]=T**e; K[b,a]=-T**e; e+=1
    assert K.T==-K and T-1>2*C*C
    R=[]
    for k in range(2*m-2):
        R.append(S.Matrix(m,m,lambda a,b:
            int(a+b==k) if a+b<2*m-2 else -p[k]))
    t=S.Symbol('t')
    P=sum(c*t**a for a,c in enumerate(p))
    # Certify the entire complex bilinear remainder identity on a basis.
    for a in range(m):
        for b in range(m):
            rhs=sum(R[k][a,b]*t**k for k in range(2*m-2))
            assert S.rem(t**(a+b)-rhs,P,t)==0
    Z=S.zeros(m)
    B=[]
    for r in R:
        B.extend([S.BlockMatrix([[r,Z],[Z,-r]]).as_explicit(),
                  S.BlockMatrix([[Z,r],[r,Z]]).as_explicit()])
    I=S.eye(n)
    B.extend([I,S.BlockMatrix([[Z,-K],[K,Z]]).as_explicit()])
    assert len(B)==j and all(b==b.T for b in B)
    identity_index=j-2
    M=1+max(sum(abs(b[a,c]) for c in range(n)) for b in B for a in range(n))
    A=[I if k==identity_index else M*I+b for k,b in enumerate(B)]
    for k,a in enumerate(A):
        assert a==a.T
        # Strict positive diagonal dominance certifies positive definiteness.
        assert all(a[r,r]>sum(abs(a[r,c]) for c in range(n) if c!=r) for r in range(n))
        assert a==I if k==identity_index else a-M*A[identity_index]==B[k]
    # The bisector equations for means 0,e_1,...,e_{j-1}.
    # Columns are (offset, first j-1 normal coordinates, final n coordinates).
    E=S.zeros(j,d0+1)
    for r in range(j): E[r,0]=-1
    for r in range(1,j): E[r,r]=1
    assert E[:,:j].det()!=0 and E[:,j:]==S.zeros(j,n)
    checked=0
    if exhaustive:
        for inds in combinations(roots,m-1):
            # One representative of each unordered factorization.
            if 1 not in inds: continue
            other=tuple(r for r in roots if r not in inds)
            u=S.Matrix(factor_vector(inds)); v=S.Matrix(factor_vector(other))
            assert mul(list(u),list(v))==p
            assert all(0<a<=C for a in list(u)+list(v))
            assert u.dot(v)>0
            wedge=[u[a]*v[b]-u[b]*v[a] for a in range(m) for b in range(a+1,m)]
            assert any(wedge) and max(map(abs,wedge))<=2*C*C
            assert (u.T*K*v)[0]!=0
            assert all((u.T*r*v)[0]==0 for r in R)
            # Extra two forms on alpha*u, beta*v have determinant nonzero:
            assert u.dot(v)*(u.T*K*v)[0]!=0
            checked+=1
        assert checked==comb(2*m-2,m-1)//2
    # Full mod-2 top Stiefel-Whitney polynomial, represented by exponents.
    monomials={(j+k,2*j-k) for k in range(j+1) if comb(j,k)%2}
    surviving={(a,b) for a,b in monomials if a<=d and b<=d}
    assert (3*n-2,3*n-4) in surviving
    assert comb(j,n)%2==1
    print(f's={s}: lower counterexample dimension {d0}; upper {d}; '
          f'factor pairs certified {checked}; surviving monomials {sorted(surviving)}')

if __name__=='__main__':
    for s in (3,4,5): check(s)
