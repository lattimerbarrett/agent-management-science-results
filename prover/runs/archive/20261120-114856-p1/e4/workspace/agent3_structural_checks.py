"""Exact structural checks for restarted CG normalized residuals.
Run with Python/SymPy. No floating-point arithmetic is used.
"""
import sympy as S
z=S.Symbol('z')
def op(nodes,w,s):
    G=S.Matrix([[sum(wi*xi**(j+k) for xi,wi in zip(nodes,w)) for k in range(s)] for j in range(s)])
    rhs=S.Matrix([-sum(wi*xi**(j+s) for xi,wi in zip(nodes,w)) for j in range(s)])
    c=G.inv()*rhs
    q=z**s+sum(c[j]*z**j for j in range(s))
    h=S.factor(sum(wi*q.subs(z,xi)**2 for xi,wi in zip(nodes,w)))
    return q,h
def step(nodes,w,s):
    q,h=op(nodes,w,s)
    return [S.factor(wi*q.subs(z,xi)**2/h) for xi,wi in zip(nodes,w)],q,h
for s in (1,2,3,4):
    nodes=list(map(S.Rational,range(1,2*s+1)))
    raw=[S.Rational((i+2)**2+1) for i in range(2*s)]
    w=[v/sum(raw) for v in raw]
    wp,q,h=step(nodes,w,s);wpp,qp,hp=step(nodes,wp,s)
    prod=S.expand(q*qp)
    assert sum(wi*prod.subs(z,xi) for xi,wi in zip(nodes,w))==h
    variance=S.factor(sum(wi*(prod.subs(z,xi)-h)**2 for xi,wi in zip(nodes,w)))
    assert variance==h*(hp-h) and hp>=h
    # Rational Stieltjes numerator and remainder factorization, n=2s.
    P=S.prod(z-xi for xi in nodes)
    M=S.expand(sum(wi*S.div(P,z-xi,z)[0] for xi,wi in zip(nodes,w)))
    Mp=S.expand(sum(wi*S.div(P,z-xi,z)[0] for xi,wi in zip(nodes,wp)))
    rem=S.rem(q*M,P,z)
    assert S.degree(rem,z)<=s-1
    assert S.Poly(rem,z).LC()==h
    assert S.expand(Mp-q*rem/h)==0
print('PASS: exact Lyapunov and Stieltjes-numerator identities for s=1,2,3,4')
# Exact feature formulation for p0(z)=z^2-5 at roots p0=+-4.
# Four positive, distinct eigenvalues after an immaterial shift if needed.
nodes=list(map(S.Rational,[-3,-1,1,3]));p0=z*z-5;h0=S.Integer(16);s=2
w=list(map(S.Rational,[S.Rational(1,10),S.Rational(2,10),S.Rational(3,10),S.Rational(4,10)]))
a=[S.Matrix([1,xi])/p0.subs(z,xi) for xi in nodes]
m=sum((wi*ai for wi,ai in zip(w,a)),S.zeros(s,1))
G=sum((wi*ai*ai.T for wi,ai in zip(w,a)),S.zeros(s))
u=G.inv()*m;d=(m.T*u)[0]
wp,q,h=step(nodes,w,s)
assert S.expand(q-(p0-sum(u[j]*z**j for j in range(s))))==0
assert h==h0*(1-d)
for wi,wpi,ai in zip(w,wp,a):
    assert wpi==S.factor(wi*(1-(ai.T*u)[0])**2/(1-d))
Huu=sum((wi*ai*(ai.T*u)[0]**2 for wi,ai in zip(w,a)),S.zeros(s,1))
mp=sum((wi*ai for wi,ai in zip(wp,a)),S.zeros(s,1))
assert mp==(-m+Huu)/(1-d)
print('PASS: exact p0^2=h0 feature reduction and normal-moment map')

# Complementary-degree reciprocal-barycentric duality.
for m in range(3,10):
    nodes=list(map(S.Rational,range(1,m+1)))
    raw=[S.Rational((i+2)**2+1) for i in range(m)]
    w=[v/sum(raw) for v in raw]
    P=S.prod(z-xi for xi in nodes)
    c=[1/S.diff(P,z).subs(z,xi) for xi in nodes]
    Z=sum(ci*ci/wi for ci,wi in zip(c,w))
    wd=[ci*ci/wi/Z for ci,wi in zip(c,w)]
    for s in range(1,m-1):
        t=m-s-1
        ws,qs,hs=step(nodes,w,s)
        wt,qt,ht=step(nodes,wd,t)
        assert ws==wt
        assert S.factor(hs*ht*Z)==1
print('PASS: exact complementary-degree reciprocal-barycentric duality for m=3,...,9')

# Exact identity giving bounded total variation of even monic polynomials.
for s in range(1,5):
    nodes=list(map(S.Rational,range(1,2*s+2)))
    raw=[S.Rational((i+2)**2+1) for i in range(len(nodes))]
    w=[v/sum(raw) for v in raw]
    wp,q,h=step(nodes,w,s)
    wpp,qp,hp=step(nodes,wp,s)
    qpp,hpp=op(nodes,wpp,s)
    e=S.expand(q*qp-h)
    for j in range(s):
        lhs=sum(wi*q.subs(z,xi)*xi**j for xi,wi in zip(nodes,wpp))
        rhs=sum(wi*q.subs(z,xi)*e.subs(z,xi)**2*xi**j for xi,wi in zip(nodes,w))/(h*hp)
        assert S.factor(lhs-rhs)==0
print('PASS: exact bounded-variation coefficient identity for s=1,...,4')
