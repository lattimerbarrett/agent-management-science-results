import sympy as s
# Exact sign obstruction for all positive radial cotangent profiles.
u=s.symbols('u',real=True); Q=s.symbols('Q',positive=True)
F=u-(2-3*u*u)*Q
assert s.simplify(F.subs(u,-s.sqrt(s.Rational(2,3)))) == -s.sqrt(s.Rational(2,3))
assert s.simplify(F.subs(u,s.sqrt(s.Rational(2,3)))) == s.sqrt(s.Rational(2,3))
print('Exact opposite-latitude signs verified:', -s.sqrt(s.Rational(2,3)),s.sqrt(s.Rational(2,3)))
open('workspace/agent2_radial_obstruction.py','w').write(open('scratchpad.py').read())
