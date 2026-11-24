import sympy as S
from pathlib import Path
x,r=S.symbols('x r');s=(5+S.sqrt(5))/2;P=x**4-5*x*x+4;h=-x**3-2*x*x+x+8;k=x*x+4*x+7;D=P*P-1;Z=x*x+r*x+(7+3*S.sqrt(5))*r-4

def deriv(p):return S.simplify(-S.Poly(S.rem((x*x-s)*P*p,D,x),x).coeff_monomial(x**7))
print('grad_hZ',deriv(h*Z));g=deriv(k*Z);print('grad_kZ',S.factor(g));sol=S.solve(g,r);print('rsolve',sol)
for rr in sol:
 ZZ=S.expand(Z.subs(r,rr));print('Z',ZZ,'disc',S.simplify(S.discriminant(ZZ,x)),S.N(S.discriminant(ZZ,x)))
