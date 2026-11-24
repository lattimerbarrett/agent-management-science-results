import sympy as s
x=s.symbols('x', positive=True)
# Extremal spectral constraints from the Gram-matrix argument, augmented
# by grouping two spectral-cut projections (a two-projection algebra).
for p in range(1,7):
 F=(1-x)**p
 L=s.integrate(F,(x,0,1))
 t=s.Rational(1,p+1)
 pair=s.simplify(2*t*F.subs(x,t))
 assert pair<=L
 print('F=(1-t)^%d'%p, 'integral=',L,'max pair-cut value=',pair,'gap=',s.simplify(L-pair))
print('The additional two-projection constraint still does not exclude these scalar models.')
