import sympy as s
z,w,t=s.symbols('z w t')
H=lambda p:s.Matrix([p[1],16*p[1]**2-p[0]/4])
# Rational arithmetic throughout.
H=lambda p:s.Matrix([p[1],16*p[1]**2-s.Rational(1,4)*p[0]])
p=s.Matrix([t,0])
expected=[s.Matrix([0,-t/4]),s.Matrix([-t/4,t*t]),s.Matrix([t*t,16*t**4+t/16])]
for q in expected:
 p=H(p).applyfunc(s.expand)
 assert p==q
print('Exact circle iterates:',[list(q) for q in expected])
J=H(s.Matrix([z,w])).jacobian([z,w])
assert J.det()==s.Rational(1,4)
assert set(J.subs({z:0,w:0}).eigenvals())=={s.I/2,-s.I/2}
print('Jacobian determinant =',J.det(),'; attracting eigenvalues =',J.subs({z:0,w:0}).eigenvals())
# Cone |w|>=max(|z|,1) maps strictly into |w_new|>|w|.
r=s.symbols('r',real=True,positive=True)
expr=16*r*r-r/4-r
assert s.expand(expr.subs(r,1+s.Symbol('u',nonnegative=True)))==16*s.Symbol('u',nonnegative=True)**2+s.Rational(123,4)*s.Symbol('u',nonnegative=True)+s.Rational(59,4)
assert 16-s.Rational(1,16)==s.Rational(255,16)>1
print('Cone expansion certified: 16 r^2-r/4-r >0 for r>=1.')
print('Classical basin theorem then gives Runge FB domain avoiding circle but containing hull point 0.')
