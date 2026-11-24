import sympy as S
from pathlib import Path
r=S.sqrt(3);u=S.symbols('u',positive=True);Q=S.symbols('Q',real=True)
c0=3-(r-1)/u
J=3*u-1/(1/(r*u)-1)+S.Rational(18,25)*(c0-S.Rational(1,4))
print('J0',S.simplify(J.subs(u,1/(2*r))))
print('J1',S.simplify(J.subs(u,S.Rational(1,3))))
print('Jsec',S.factor(S.diff(J,u,2)))
print('eps threshold',S.sqrt(S.Rational(108,205)).evalf(),S.Rational(18,25))
T=Q/S.Integer(4)-S.Rational(1,9)*(S.Rational(205,81)*Q*Q-S.Rational(4,3))
print('Tends',S.factor(T.subs(Q,S.Rational(18,25))),S.factor(T.subs(Q,S.Rational(11,9))))
