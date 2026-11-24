import sympy as s
x=s.symbols('x',positive=True)
a=(x+s.Rational(1,2))**2/x**2
L=x-s.Rational(1,4)
U=L+1/(32*x)+1/(64*x**2)
lower_residual=s.factor(a*L-L.subs(x,x+1))
upper_residual=s.factor(a*U-U.subs(x,x+1))
assert lower_residual == -1/(16*x**2)
assert s.factor(upper_residual-(6*x**3+9*x**2+8*x+1)/(256*x**4*(x+1)**2))==0
assert all(c>0 for c in s.Poly(6*x**3+9*x**2+8*x+1,x).all_coeffs())
print('PASS: recurrence residuals certify L<Gamma(x+1/2)^2/Gamma(x)^2<U for x>1/4')
print('Lower residual:',lower_residual)
print('Upper residual:',upper_residual)
from pathlib import Path
Path('workspace/agent4_gamma_bounds.py').write_text(Path('scratchpad.py').read_text())
