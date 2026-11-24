import sympy as s
S,t=s.symbols('S t', nonnegative=True)
mu=(S-2*t+s.sqrt((S-2*t)**2+12*t*t))/6
assert s.simplify(3*mu**2-(S-2*t)*mu-t*t)==0
# At w=0 and S>0, the transverse complex Levi eigenvalue is mu_t.
Sp=s.symbols('Sp',positive=True)
assert s.simplify(mu.subs(t,0))==S/3
assert s.simplify(s.diff(mu,t).subs(S,Sp).subs(t,0))==-s.Rational(2,3)
assert s.simplify(s.diff(mu,S).subs(S,Sp).subs(t,0))==s.Rational(1,3)
lam=s.symbols('lam',positive=True)
assert s.simplify(mu.subs({S:lam*S,t:lam*t},simultaneous=True)-lam*mu)==0
print('PASS: explicit homogeneous Minkowski-square formula and mixed Levi at w=0.')
