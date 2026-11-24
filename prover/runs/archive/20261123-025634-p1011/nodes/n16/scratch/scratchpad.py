import sympy as s
x=s.symbols('x', real=True)
m=s.symbols('m', integer=True, positive=True)
# Flat ambient metric; boundary graph x_n = x_1^(2k).
# Its only possibly nonzero principal curvature is kappa.
for k in (2,3,4):
    f=x**(2*k)
    kappa=s.diff(f,x,2)/(1+s.diff(f,x)**2)**s.Rational(3,2)
    norm2=s.factor((m-1)/m*kappa**2)
    print('k =', k)
    print('|trace-free II|^2 =', norm2)
    print('leading term:', s.series(norm2,x,0,4*k-3))
