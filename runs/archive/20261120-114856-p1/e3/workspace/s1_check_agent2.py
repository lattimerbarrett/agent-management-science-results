import sympy as sp
from pathlib import Path
m3,m4,V=sp.symbols('m3 m4 V', real=True)
t=sp.symbols('t',real=True)
q=(t*t-m3*t/V-V)**2
moments={0:1,1:0,2:V,3:m3,4:m4}
Eq=sp.expand(sum(coef*moments[pow[0]] for pow,coef in sp.Poly(q,t).terms()))
assert sp.simplify(Eq-(m4-m3*m3/V-V*V))==0
# Exact rational checks: normalization, monotonicity, equality on all two-point measures.
def T(lam,p):
    mu=sum(a*b for a,b in zip(lam,p))
    var=sum(b*(a-mu)**2 for a,b in zip(lam,p))
    return [sp.cancel(b*(a-mu)**2/var) for a,b in zip(lam,p)]
def variance(lam,p):
    mu=sum(a*b for a,b in zip(lam,p))
    return sum(b*(a-mu)**2 for a,b in zip(lam,p))
checks=0
for n in range(2,8):
    lam=[sp.Integer(i*i+1) for i in range(n)]
    p=[sp.Rational(i+1,n*(n+1)//2) for i in range(n)]
    for k in range(4):
        q=T(lam,p)
        assert sum(q)==1
        assert variance(lam,q)>=variance(lam,p)
        p=q; checks+=1
for a in range(1,6):
    for b in range(a+1,7):
        for j in range(1,10):
            p=[sp.Rational(j,10),sp.Rational(10-j,10)]
            assert T([a,b],T([a,b],p))==p
            checks+=1
print('Exact algebra and',checks,'rational dynamical checks passed.')
Path('workspace/s1_check_agent2.py').write_text(Path(__file__).read_text())
