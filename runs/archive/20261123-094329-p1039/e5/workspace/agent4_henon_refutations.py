import sympy as S
z,w=S.symbols('z w')
a=S.Rational(1,4)
H=S.Matrix([z*z+a*w,a*z])
zin,win=S.symbols('Z W')
inv=S.Matrix([win/a,(zin-(win/a)**2)/a])
assert H.subs({z:inv[0],w:inv[1]}, simultaneous=True)==S.Matrix([zin,win])
J=H.jacobian([z,w])
assert S.factor(J.det())==-a*a
assert J.subs({z:0,w:0}).eigenvals()=={a:1,-a:1}
# Cone r=|z|>=2, |w|<=r. Bound |H_1|>=r^2-r/4.
u=S.symbols('u',nonnegative=True)
r=2+u
assert S.expand(r*r-a*r-S.Rational(7,4)*r)==u*u+2*u
assert S.expand(r*r-a*r-a*r)==u*u+S.Rational(7,2)*u+3
# Uniform compact neighborhood around wall |z|=2, |w|<=2:
# |z|>=19/10 and |w|<=21/10 maps directly into escape cone.
lo=S.Rational(19,10)**2-a*S.Rational(21,10)
hi=a*S.Rational(21,10)
assert lo>2 and lo>hi
# Local Koenigs linearization contraction bound on Euclidean ball radius1/16.
# ||H(v)|| <= (a+1/16)||v||, q^2/a<1 ensures convergence A^-k H^k.
q=a+S.Rational(1,16)
assert q*q/a<1
print('H inverse, determinant, attracting eigenvalues and escape cone checked exactly.')
print('Uniform-neighborhood first-coordinate lower bound:',lo)
print('Koenigs convergence ratio bound:',q*q/a)
open('workspace/agent4_henon_refutations.py','w').write(open('scratchpad.py').read())