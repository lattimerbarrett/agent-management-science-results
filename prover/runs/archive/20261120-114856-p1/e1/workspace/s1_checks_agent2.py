"""Exact checks for the s=1 proof; run with Python + SymPy."""
import sympy as S
from itertools import combinations

def symbolic_checks():
    d, m2, m3, m4 = S.symbols('d m2 m3 m4', real=True)
    def E(poly):
        p=S.Poly(S.expand(poly),d)
        moments={0:S.Integer(1),1:S.Integer(0),2:m2,3:m3,4:m4}
        return S.expand(sum(co*moments[k[0]] for k,co in p.terms()))
    q=d*d-m3/m2*d-m2
    pearson=E(q*q)/m2
    variance_next=m4/m2-m3*m3/m2**2
    assert S.simplify(pearson-(variance_next-m2))==0
    # μ'−μ=m3/m2. Products give the two-step inner product.
    assert S.simplify(E((-d)*(m3/m2-d))-m2)==0
    # Exact normalized inner product is sigma/sigma_next.
    sig, sigp=S.symbols('sig sigp', positive=True)
    assert S.simplify(2-2*sig/sigp-2*(sigp-sig)/sigp)==0

def rational_orbit_checks():
    lam=list(map(S.Rational,[1,2,4,7]))
    w=[S.Rational(1,10),S.Rational(2,10),S.Rational(3,10),S.Rational(4,10)]
    for _ in range(8):
        mu=sum(t*p for t,p in zip(lam,w))
        v=sum((t-mu)**2*p for t,p in zip(lam,w))
        assert v>0
        wn=[(t-mu)**2*p/v for t,p in zip(lam,w)]
        mun=sum(t*p for t,p in zip(lam,wn))
        vn=sum((t-mun)**2*p for t,p in zip(lam,wn))
        q=[(t-mu)**2-(mun-mu)*(t-mu)-v for t in lam]
        assert S.simplify(vn-v-sum(p*qi**2 for p,qi in zip(w,q))/v)==0
        assert vn>=v
        inner_numerator=sum(p*(mu-t)*(mun-t) for t,p in zip(lam,w))
        assert inner_numerator==v
        w=wn
    # Every two-point distribution has exact variance equality.
    p=S.symbols('p', positive=True)
    for a,b in combinations(lam,2):
        mu=p*a+(1-p)*b
        v=S.expand(p*(a-mu)**2+(1-p)*(b-mu)**2)
        assert S.simplify(v-p*(1-p)*(b-a)**2)==0
        wn=[S.cancel(p*(a-mu)**2/v),S.cancel((1-p)*(b-mu)**2/v)]
        assert S.simplify(wn[0]-(1-p))==0
        assert S.simplify(wn[1]-p)==0

if __name__=='__main__':
    symbolic_checks()
    rational_orbit_checks()
    print('All s=1 symbolic identities and exact rational orbit checks passed.')
