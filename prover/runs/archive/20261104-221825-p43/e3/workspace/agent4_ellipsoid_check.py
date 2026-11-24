import sympy as s
from pathlib import Path
# General axis-scaling radial map h(x)=diag(A(r)/r,B(r)/r,...)*x.
r,A,B,Ap,Bp=s.symbols('r A B Ap Bp',positive=True)
x=s.Matrix(s.symbols('x0:4',real=True));scales=[A/r]+[B/r]*3;derivs=[Ap/r-A/r**2]+[Bp/r-B/r**2]*3
D=s.diag(*scales);u=s.Matrix([derivs[i]*x[i] for i in range(4)]);J=D+u*(x.T/r)
formula=A*B**3/r**5*(Ap/A*x[0]**2+Bp/B*(x[1]**2+x[2]**2+x[3]**2))
# Off the symbolic sphere constraint sum x_i²=r², determinant identity modulo that constraint.
err=s.factor((J.det()-formula)*r**6/(B**2))
print('determinant identity residual factor:',err)
assert s.rem(s.Poly(s.together(J.det()-formula).as_numer_denom()[0],x[3]),s.Poly(sum(t*t for t in x)-r*r,x[3])).as_expr()==0
# Equivalent polar form: det = A B³/r³ [A'/A theta1²+B'/B(1−theta1²)] >0.
t=s.symbols('t',real=True)
polar=A*B**3/r**3*(Ap/A*t+Bp/B*(1-t))
assert s.simplify(formula.subs({x[0]**2:r*r*t,x[1]**2:r*r*(1-t),x[2]:0,x[3]:0})-polar)==0
print('Positive ellipsoid-foliation Jacobian formula checked exactly.')
code=Path('scratchpad.py').read_text().replace("",'')
