from itertools import combinations
from math import comb
import sympy as S


def polynomial_product(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out


def factor_from_roots(roots):
    f=[1]
    for r in roots: f=polynomial_product(f,[-r,1])
    return f


def certificate(s, enumerate_factors=True):
    assert s>=3
    n=2**(s-1); k=n//2; L=2*k-2; j=2*n-2
    roots=[2**i for i in range(L)]
    p=factor_from_roots(roots)
    assert len(p)==L+1 and p[-1]==1
    I=S.eye(n); Z=S.zeros(k)
    T=S.zeros(k); T[0,1]=1; T[1,0]=-1
    H2=Z.row_join(-T).col_join(T.row_join(Z))
    C=[I,H2]
    for r in range(L):
        M=S.Matrix(k,k,lambda a,b:int(a+b==r)-p[r]*int(a==k-1 and b==k-1))
        C.append(M.row_join(Z).col_join(Z.row_join(-M)))
        C.append(Z.row_join(M).col_join(M.row_join(Z)))
    assert len(C)==j
    A=[I]
    for B in C[1:]:
        assert B==B.T
        lam=1+max(sum(abs(B[a,b]) for b in range(n)) for a in range(n))
        Q=lam*I+B
        assert all(Q[a,a]>sum(abs(Q[a,b]) for b in range(n) if a!=b) for a in range(n))
        A.append(Q)
    # Verify every coefficient of the real bilinear map using basis pairs.
    for a in range(n):
        for b in range(n):
            # SymPy's I, rather than floating-point complex arithmetic.
            x=[S.Integer(0)]*k; y=[S.Integer(0)]*k
            x[a%k]=1 if a<k else S.I
            y[b%k]=1 if b<k else S.I
            q=polynomial_product(x,y)
            rem=[S.expand(q[r]-q[L]*p[r]) for r in range(L)]
            h2=S.re(S.I*(S.conjugate(x[0])*y[1]-S.conjugate(x[1])*y[0]))
            expected=[int(a==b),h2]
            for z in rem: expected.extend([S.re(z),S.im(z)])
            assert [B[a,b] for B in C]==expected
    checked=0
    if enumerate_factors:
        for inds in combinations(range(L),k-1):
            selected=set(inds)
            f=factor_from_roots([roots[i] for i in inds])
            g=factor_from_roots([roots[i] for i in range(L) if i not in selected])
            assert polynomial_product(f,g)==p
            assert all(f[a]*g[a]>0 for a in range(k))
            inner=sum(f[a]*g[a] for a in range(k))
            wronskian=f[0]*g[1]-f[1]*g[0]
            signed_binary=sum((1 if i in selected else -1)*2**(L-1-i) for i in range(L))
            assert signed_binary%2==1
            assert wronskian*2**(L-1)==p[0]*signed_binary
            assert inner>0 and wronskian!=0
            checked+=1
        assert checked==comb(L,k-1)
    # Euler-class coefficient and all dimension identities.
    J=2*n-1; D=3*n-1
    assert 3*J==(D-1)+D
    assert (D-1)-J==n-1
    assert comb(J,n-1)%2==1
    assert (3*n-3)-(j-1)==n
    assert len(A)==j
    return dict(s=s,n=n,j=j,answer=3*n-2,matrices=len(A),matrix_size=n,
                factor_splits_checked=checked,euler_parity=comb(J,n-1)%2)

if __name__=='__main__':
    for s in (3,4,5): print(certificate(s))
