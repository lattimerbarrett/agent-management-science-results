"""Canonical ring factors and checks of proved structural identities.
Numerics are verification, not proof of the unproved global determinant claim.
"""
import numpy as np

def ring_factors(m,r,R,d):
    z=np.exp(2j*np.pi*np.arange(m)/m)
    D=d+np.sqrt(d*d+np.abs(R*z-r)**2)
    c=(R*z.conjugate()-r)/D
    b=(R-r*z)/D
    H=np.array([1.],complex)
    A=np.array([1.],complex)
    B=np.array([1.],complex)
    for k in range(1,m):
        H=np.convolve(H,[1,1j*np.exp(-1j*np.pi*k/m)])
    for k in range(m):
        A=np.convolve(A,[1,-c[k]])
        B=np.convolve(B,[b[k],1])
    return z,D,c,b,H,A,B

def check(m,r,R,d):
    z,D,c,b,H,A,B=ring_factors(m,r,R,d)
    c0=c[0].real
    assert abs(c0.imag if hasattr(c0,'imag') else 0)<1e-12
    assert 0<c0<1
    assert np.max(abs(c-z.conjugate()*b))<1e-12
    assert np.max(abs((R*z-r)*c*c+2*d*c-(R*z.conjugate()-r)))<1e-11*R
    if m>1:
        assert np.all(c[1:].real<c0+1e-12)
        assert np.all(abs(c[1:])>c0-1e-12)
    h=np.array([np.prod([1/np.tan(j*np.pi/(2*m)) for j in range(1,k+1)]) for k in range(m)])
    assert np.max(abs(H-h))<1e-8*max(h)
    assert min(H.real)>0 and max(abs(H.imag))<1e-8*max(abs(H))
    assert min(B.real)>0 and max(abs(B.imag))<1e-8*max(abs(B))
    # The Möbius-transformed cross factor (k=0 becomes constant).
    Q=np.array([1.],complex)
    for k in range(1,m):
        Q=np.convolve(Q,[1,c0-c[k]])
    assert min(Q.real)>0
    assert max(abs(Q.imag))<1e-8*max(abs(Q))
    return True

if __name__=='__main__':
    rng=np.random.default_rng(327)
    count=0
    for m in range(1,41):
        for trial in range(100):
            r=np.exp(rng.uniform(-6,-.001))
            d=np.exp(rng.uniform(-6,6))
            check(m,r,1.,d)
            count+=1
    print('Verified canonical identities and proved sign inequalities in',count,'samples')


def exact_section_lemma_tests():
    """Exact checks of the general LC-short-factor section inequality.
    For h positive LC of degree m-1 and C arbitrary positive degree m,
    p=h*C has p[q]*p[q+m+1] < p[q+1]*p[q+m].
    """
    from fractions import Fraction as F
    from random import Random
    rng=Random(814)
    count=0
    for m in range(2,21):
        for trial in range(100):
            ratios=sorted([F(rng.randint(1,10),rng.randint(1,10)) for _ in range(m-1)], reverse=True)
            h=[F(1)]
            for r in ratios:h.append(h[-1]*r)
            C=[F(rng.randint(1,20)) for _ in range(m+1)]
            p=[sum((h[i]*C[j] for i in range(m) for j in range(m+1) if i+j==e),F(0)) for e in range(2*m)]
            for q in range(m-1):
                assert p[q]*p[q+m+1]<p[q+1]*p[q+m]
                # Verify every shared monomial has nonpositive coefficient.
                for i in range(q+1):
                    for j in range(q+2,m+1):
                        a=q-i;b=q+m-j
                        assert h[a]*h[b+1]<=h[a+1]*h[b]
                count+=1
    return count


def check_tree_identity(m,r,R,d,dps=60):
    """High precision check of the proved matrix-tree representation of Q_A."""
    import mpmath as mp
    with mp.workdps(dps):
        r,R,d=map(mp.mpf,(r,R,d))
        zz=[mp.exp(2j*mp.pi*k/m) for k in range(m)]
        cc=[(R*mp.conj(z)-r)/(d+mp.sqrt(d*d+abs(R*z-r)**2)) for z in zz]
        coeff=[sum(cc[k]*zz[k]**(-j) for k in range(m))/m for j in range(m)]
        tol=mp.mpf(10)**(-dps+15)
        assert max(abs(mp.im(v)) for v in coeff)<tol
        coeff=[mp.re(v) for v in coeff]
        assert all(coeff[j+1]>coeff[j] for j in range(m-1))
        S=mp.matrix(m)
        for j in range(m):S[(j+1)%m,j]=1
        C=mp.matrix(m)
        for i in range(m):
            for j in range(m):C[i,j]=coeff[(i-j)%m]
        D=mp.eye(m)-S;L=-D*C
        assert all(L[i,j]<0 for i in range(m) for j in range(m) if i!=j)
        for t in [mp.mpf('.2'),mp.mpf('1.1'),mp.mpc('.3','.7')]:
            mat=D+t*L
            minor=mp.matrix([[mat[i,j] for j in range(m-1)] for i in range(m-1)])
            q=mp.fprod(1-cc[k]*t for k in range(1,m))
            assert abs(mp.det(minor)-q)<tol*max(1,abs(q))
        return True
