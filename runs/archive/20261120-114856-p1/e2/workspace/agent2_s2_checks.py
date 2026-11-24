"""Exact rational checks for spectral restart maps and n=s+2 formula."""
import sympy as S

def step(lam,w,s):
    n=len(lam)
    H=S.Matrix(s,s,lambda j,k:sum(w[i]*lam[i]**(j+k) for i in range(n)))
    v=S.Matrix([sum(w[i]*lam[i]**(j+s) for i in range(n)) for j in range(s)])
    coeff=H.inv()*(-v)
    q=[lam[i]**s+sum(coeff[j]*lam[i]**j for j in range(s)) for i in range(n)]
    h=sum(wi*qi**2 for wi,qi in zip(w,q))
    return [S.factor(wi*qi**2/h) for wi,qi in zip(w,q)],q,S.factor(h)

def dual_theta(lam,w):
    d=[1/S.prod(lam[i]-lam[j] for j in range(len(lam)) if j!=i) for i in range(len(lam))]
    z=[di**2/wi for di,wi in zip(d,w)]; Z=sum(z)
    z=[zi/Z for zi in z]
    return S.factor(sum(li*zi for li,zi in zip(lam,z))),z

def check():
    # arbitrary rational positive spectra and weights, not a symmetric special case
    for s in [1,2,3]:
        lam=list(map(S.Integer,range(1,s+3)))
        den=sum(range(2,len(lam)+2));w=[S.Rational(j,den) for j in range(2,len(lam)+2)]
        wp,q,h=step(lam,w,s);wpp,qp,hp=step(lam,wp,s)
        a,z=dual_theta(lam,w); b,zp=dual_theta(lam,wp);c,_=dual_theta(lam,wpp)
        V=sum(zi*(li-a)**2 for li,zi in zip(lam,z))
        expected=[S.factor(zi*(li-a)**2/V) for li,zi in zip(lam,z)]
        assert wp==expected
        B=sum(wi/(li-a) for li,wi in zip(lam,w));C=sum(wi/(li-a)**2 for li,wi in zip(lam,w))
        assert S.factor(b-a-B/C)==0
        denominator=sum(zi*((li-a)/(li-b))**2 for li,zi in zip(lam,z))
        numerator=sum(zi*(li-a)/(li-b) for li,zi in zip(lam,z))
        assert S.factor(c-b-(b-a)*numerator/denominator)==0
        # Two-step weight formula.
        factor=1-B**2/C
        for i in range(len(lam)):
            assert S.factor(wpp[i]-w[i]*((lam[i]-b)/(lam[i]-a))**2/factor)==0
    # T^2 is identity on each (s+1)-point face, all s.
    for s in [1,2,3,4]:
        lam=list(map(S.Integer,range(1,s+2)))
        den=sum(range(2,len(lam)+2));w=[S.Rational(j,den) for j in range(2,len(lam)+2)]
        wp,_,_=step(lam,w,s);wpp,_,_=step(lam,wp,s)
        assert wpp==w
    print('Exact dual-map, theta recurrence, two-step, and minimal-face identities passed.')

if __name__=='__main__':check()
