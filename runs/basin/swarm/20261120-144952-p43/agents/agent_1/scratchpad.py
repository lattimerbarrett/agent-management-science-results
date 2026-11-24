import sympy as s

# H(x,y)=x.y-x_3+y_1 on S^2 x S^2.
x1,x2,x3,y1,y2,y3,lam,mu=s.symbols('x1 x2 x3 y1 y2 y3 lam mu', real=True)
x=s.Matrix([x1,x2,x3]); y=s.Matrix([y1,y2,y3])
e1=s.Matrix([1,0,0]); e3=s.Matrix([0,0,1])
H=x.dot(y)-x3+y1
F1=(y-e3).cross(x); F2=(x+e1).cross(y)
assert s.expand(x.dot(F1))==0
assert s.expand(y.dot(F2))==0

# Check omega(X_H,v)=dH(v), modulo tangency and unit norms.
v=s.Matrix(s.symbols('v1:4')); w=s.Matrix(s.symbols('w1:4'))
for u,A,V,F in [(x,y-e3,v,F1),(y,x+e1,w,F2)]:
    err=s.expand(u.dot(F.cross(V))-A.dot(V))
    expected=s.expand((u.dot(u)-1)*A.dot(V)-u.dot(A)*u.dot(V))
    assert s.expand(err-expected)==0
print('Vector-field formula, tangency, and sign convention: checked.')

# Critical point equations, with Lagrange multipliers.
variables=[x1,x2,x3,y1,y2,y3,lam,mu]
eqs=list(y-e3-lam*x)+list(x+e1-mu*y)+[x.dot(x)-1,y.dot(y)-1]
G=s.groebner(eqs,*variables,order='lex')
expected=[-mu**2+2*x1+2, x2, mu**3-2*mu+2*x3,
          2*lam-mu**3+2*y1, y2, mu**2+2*y3-2,
          lam**2-mu**2, 2*lam*mu-mu**4+mu**2, mu**5-3*mu**3]
assert [p.as_expr() for p in G.polys]==expected
print('Exact Groebner basis:')
for p in expected:
    print(' ',p)

solutions=[]
for m in [s.Integer(0),s.sqrt(3),-s.sqrt(3)]:
    ell=m
    xx=s.Matrix([-1,0,0]) if m==0 else s.Matrix([s.Rational(1,2),0,-m/2])
    yy=s.Matrix([0,0,1]) if m==0 else s.Matrix([m/2,0,-s.Rational(1,2)])
    subst=dict(zip(variables,list(xx)+list(yy)+[ell,m]))
    assert all(s.simplify(p.subs(subst))==0 for p in eqs)
    solutions.append(subst)
    print('Critical point:',tuple(xx),tuple(yy),'; H =',s.simplify(H.subs(subst)))
assert len(solutions)==3
# Completeness: elimination forces mu in {0,+sqrt(3),-sqrt(3)};
# first six basis equations determine x,y from mu,lam;
# mu=0 forces lam=0, otherwise 2*lam*mu=mu^4-mu^2 forces lam=mu.
assert s.factor(expected[-1])==mu**3*(mu**2-3)
assert s.simplify((mu**4-mu**2-2*mu**2).subs(mu**2,3))==0

# Derivative norm bound ||DF|| <= 3 on B^3 x B^3:
# ||dF1|| <= 2||dx||+||dy||; ||dF2|| <= ||dx||+2||dy||.
a,b=s.symbols('a b',nonnegative=True)
assert s.expand(9*(a*a+b*b)-((2*a+b)**2+(a+2*b)**2)-4*(a-b)**2) == 0
assert 3 < 2*s.pi
print('Derivative-norm bound 3 verified algebraically.')
print('Wirtinger inequality then excludes every nonconstant 1-periodic orbit: 2*pi > 3.')
print('Therefore the time-one map has exactly the three listed fixed points.')
