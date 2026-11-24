import sympy as s
T=s.symbols('t');eps=[T,-T,0,0];ss=sum(z*z for z in eps)
y=s.Matrix([s.Rational(1,4)+s.Rational(3,2)*z+s.Rational(9,2)*z*z-s.Rational(9,8)*ss for z in eps])
def tr(x):return s.series(x,T,0,3).removeO().expand()
a=s.Matrix([tr(z*(1-z)) for z in y]);b=s.Matrix([1-2*z for z in y]);ab=s.Matrix([tr(u*v) for u,v in zip(a,b)])
p=s.Matrix([s.Rational(1,4)+z for z in eps]);den=sum(a)
V=(s.diag(*ab)-ab*p.T-p*ab.T+sum(ab)*(p*p.T))/den
V=V.applyfunc(tr)
det=tr(V[:3,:3].det());pp=tr(s.prod(p))
logA=s.series((s.log(pp)-s.log(det))/2,T,0,3).removeO().expand()
sx=tr(sum(z/(1-z) for z in y))
assert logA.coeff(T,2)/2==s.Rational(3,2)
assert sx.coeff(T,2)/2==s.Rational(16,3)
print('r4 independent saddle amplitude check: B_H=3/2, B_omit=16/3')
