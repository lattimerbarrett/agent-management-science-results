from pathlib import Path
import sympy as s
u,t=s.symbols('u t')
H=s.Matrix([t,16*t*t-u/4])
J=H.jacobian([u,t])
assert s.simplify(J.det())==s.Rational(1,4)
assert set(J.subs({u:0,t:0}).eigenvals())=={s.I/2,-s.I/2}
W=s.symbols('W', positive=True)
escape_excess=16*W**2-W/4-W
assert s.factor(escape_excess)==W*(64*W-5)/4
v=s.symbols('v', nonnegative=True)
assert s.simplify((escape_excess-s.Rational(59,4)*W).subs(W,1+v)-16*v*(v+1))==0
# If each of two normal coordinates is bounded by eps*R and eps=d/(4R),
# then squared distance to the safe plane is at most d²/8 < d².
d,R=s.symbols('d R',positive=True)
eps=d/(4*R)
assert s.simplify(2*(eps*R)**2)==d*d/8
assert s.simplify(d*d-2*(eps*R)**2)==7*d*d/8
print('H determinant:',s.factor(J.det()))
print('H eigenvalues at 0:',list(J.subs({u:0,t:0}).eigenvals()))
print('Escape excess:',s.factor(escape_excess))
print('Two-horn distance margin:',s.simplify(d*d-2*(eps*R)**2))
