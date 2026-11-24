import sympy as s
# Exact checks of the bounded graph-gluing algebra.
I=s.eye(2); Z=s.zeros(2); h=s.diag(1,1,0,0)
x=s.Matrix([[1,s.Rational(1,2)],[0,s.Rational(1,3)]])
e1=s.diag(1,0)
def graph(e,y):
    v=e.col_join(y)
    return s.simplify(v*(I+y.T*y).inv()*v.T)
r1=graph(e1,x*e1); r=graph(I,x)
assert r*r==r and r1*r1==r1 and r*r1==r1 and r1*r==r1
assert s.simplify(r[2:4,0:2]*r[0:2,0:2].inv())==x
# Graph angle bound with C=2, checked by all principal minors.
from itertools import combinations
A=s.simplify(r*h*r-s.Rational(1,5)*r)
for k in range(1,5):
    for inds in combinations(range(4),k):
        assert A.extract(inds,inds).det()>=0
# Affine interpolation weights sum to 1 minus the residual coefficient.
for n in range(1,8):
    ts=s.symbols('t:'+str(n))
    residual=s.prod(1-t for t in ts)
    weights=[ts[j]*s.prod(1-ts[k] for k in range(j+1,n)) for j in range(n)]
    assert s.expand(sum(weights)+residual-1)==0
print('Exact graph identities and interpolation-weight identities passed.')
