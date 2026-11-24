import sympy as s
eta,t,k,r=s.symbols('eta t k r',positive=True)
print('Scaling:',s.simplify(t*eta))
print('k-fold diagonal with normalized matrix quasitrace:',s.simplify(k*eta/k))
print('single matrix corner with normalized matrix quasitrace:',eta/k)
print('renormalization inside a corner of quasitrace r:',eta/r)
print('To reach 1/2 by corner normalization one needs r =',s.solve(s.Eq(eta/r,s.Rational(1,2)),r))
