import sympy as S
# Exact nontrivial instance of extreme-root ordering and its Rayleigh witness.
x=list(map(S.Integer,[-3,-1,1,3]));nu=[S.Rational(3,16),S.Rational(5,16),S.Rational(5,16),S.Rational(3,16)]
f=lambda z:z*z-4
assert sum(w*f(z) for z,w in zip(x,nu))==0
assert sum(w*z*f(z) for z,w in zip(x,nu))==0
c1=S.Rational(-5,2);c2=S.Rational(11,5)
g=lambda z:(z-c1)*(z-c2)
mu=[w*f(z)**2/g(z)**2 for z,w in zip(x,nu)]
for c,sgn in [(c1,-1),(c2,1)]:
    raynum=sum(w*f(z)**2/(z-c) for z,w in zip(x,nu))
    ell=[g(z)/(z-c) for z in x]
    den=sum(w*t*t for w,t in zip(mu,ell))
    actual=sum(w*(z-c)*t*t for z,w,t in zip(x,mu,ell))
    assert S.factor(actual-raynum)==0
    assert sgn*raynum>0
    print('c=',c,'Rayleigh quotient minus c=',S.factor(raynum/den),'correct sign=',sgn)
# Full exact quadratic fit under mu, and evaluate h(c)'s signs.
V=S.Matrix([[1,z] for z in x]);M=V.T*S.diag(*mu)*V
coef=-M.inv()*V.T*S.Matrix([w*z*z for z,w in zip(x,mu)])
z=S.symbols('z');h=z*z+coef[1]*z+coef[0]
assert h.subs(z,c1)<0 and h.subs(z,c2)<0
print('Exact h(c1)<0 and h(c2)<0 certify h has roots beyond both test roots.')
