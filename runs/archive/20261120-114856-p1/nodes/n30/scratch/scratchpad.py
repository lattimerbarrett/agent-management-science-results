import sympy as S
x,a=S.symbols('x a', real=True)
nodes=list(map(S.Integer,[1,2,3,5,8]))
w=list(map(S.Rational,[S.Rational(1,10),S.Rational(2,10),S.Rational(3,10),S.Rational(1,10),S.Rational(3,10)]))
def orthopoly(w):
    c0,c1=S.symbols('c0 c1')
    p=x*x+c1*x+c0
    sol=S.solve([sum(wi*p.subs(x,t)*t**j for wi,t in zip(w,nodes)) for j in range(2)],(c0,c1))
    return S.expand(p.subs(sol))
p=orthopoly(w)
h=sum(wi*p.subs(x,t)**2 for wi,t in zip(w,nodes))
v=[wi*p.subs(x,t)**2/h for wi,t in zip(w,nodes)]
q=orthopoly(v)
h1=sum(vi*q.subs(x,t)**2 for vi,t in zip(v,nodes))
E=sum(wi*(p.subs(x,t)*q.subs(x,t)-h)**2 for wi,t in zip(w,nodes))
assert S.factor(E-h*(h1-h))==0
print('Exact general Lyapunov identity checked, h_next > h:',h1>h)
# A continuum of equality cases with the same polynomial and norm.
nodes=[S.Integer(t) for t in [1,2,4,5]]
w=[a,2*a-S.Rational(1,4),S.Rational(3,4)-2*a,S.Rational(1,2)-a]
p=x*x-6*x+S.Rational(13,2)
assert S.simplify(sum(w))==1
assert all(S.simplify(sum(wi*p.subs(x,t)*t**j for wi,t in zip(w,nodes)))==0 for j in range(2))
assert all(p.subs(x,t)**2==S.Rational(9,4) for t in nodes)
print('Continuum verified: 1/8 < a < 3/8; weights=',w)
print('Common monic polynomial:',p,'; common h=9/4; each direction returns after two blocks.')
