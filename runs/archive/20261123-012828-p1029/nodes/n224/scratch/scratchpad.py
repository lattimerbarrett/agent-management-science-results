import sympy as s
eta,r,t=s.symbols('eta r t', positive=True)
print('Corner increment:', eta/r)
print('Gain over original:', s.factor(eta/r-eta))
print('Normalized half-bound:', s.factor(s.Rational(1,2)-eta/r))
print('Scaling back to target t:', s.simplify((t*r/eta)*(eta/r)))
print('Thus r>=2 eta is necessary, and r<1 gives amplification; r=1 gives none.')
