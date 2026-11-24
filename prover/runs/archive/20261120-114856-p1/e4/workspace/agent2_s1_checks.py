from pathlib import Path
import sympy as S

# Symbolic Gram/Pearson identity proving the s=1 Lyapunov inequality.
V, m3, m4 = S.symbols('V m3 m4', positive=True)
G = S.Matrix([[1,0,V],[0,V,m3],[V,m3,m4]])
assert S.expand(G.det() - (V*m4-m3**2-V**3)) == 0
# Gram matrix belongs to 1, lambda-mu, (lambda-mu)^2. Its determinant
# is nonnegative, and zero iff the support has at most two points.

# Check a genuine three-node rational steepest-descent residual orbit.
lam = list(map(S.Rational,[1,2,5]))
w = list(map(S.Rational,[S.Rational(1,5),S.Rational(3,10),S.Rational(1,2)]))
def step(w):
    mu=sum(x*t for x,t in zip(lam,w))
    var=sum(t*(x-mu)**2 for x,t in zip(lam,w))
    return [S.cancel(t*(x-mu)**2/var) for x,t in zip(lam,w)]
def variance(w):
    mu=sum(x*t for x,t in zip(lam,w))
    return S.cancel(sum(t*(x-mu)**2 for x,t in zip(lam,w)))
for k in range(8):
    wn=step(w)
    mu=sum(x*t for x,t in zip(lam,w))
    v=variance(w)
    t3=sum(t*(x-mu)**3 for x,t in zip(lam,w))
    t4=sum(t*(x-mu)**4 for x,t in zip(lam,w))
    assert S.cancel(variance(wn)-v-(v*t4-t3**2-v**3)/v**2)==0
    assert variance(wn)>=v
    w=wn

# Exact involution on two nodes, checked symbolically for arbitrary masses.
a,b,p=S.symbols('a b p', real=True)
mu=p*a+(1-p)*b
var=p*(a-mu)**2+(1-p)*(b-mu)**2
pnext=S.factor(p*(a-mu)**2/var)
assert S.simplify(pnext-(1-p))==0
print('Exact symbolic Gram identity, rational Lyapunov checks, and two-node involution: PASS')
