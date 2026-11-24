import sympy as s
from pathlib import Path
r,n=s.symbols('r n',positive=True)
m=n-1
C=(n-2)**2/(4*(n-1))
B=C*(r*r-1)/(1+r*r)**m
A=2*m*B/(1+r*r)
# Bulk integrand after twice integrating the general linear source against dilation mode.
bulk=s.simplify(A+(m*A+r*s.diff(A,r))+s.diff(B,r,2)+(m-1)*s.diff(B,r)/r)
assert bulk==0
assert s.simplify(-s.diff(B,r)-r*A+2*C*r/(1+r*r)**m)==0
print('Exact arbitrary-graph dilation-source identity verified:')
print('integral S_F Z = C*(1+R^2)^(-(n-1))* integral_rim ((R^2-1)*d_r F - 2R*F).')
# Kelvin leading rim relation at arbitrary radius, F'(physical radius).
# f_K(R)=R^2 F(1/R); f_K'(R)=2R F(1/R)-F'(1/R).
# scaled F_e(R)=eps^-1 F(eps R), derivative F_e'=F'(epsR)
# divide source projection by eps^(n-2), R=rphys/eps and eps->0 gives
# C*(rphys^(3-n)*F'(rphys)-2*rphys^(2-n)*F(rphys)) angular integral,
# the negative of C*Kelvin rim integral.
eps,rho=s.symbols('eps rho',positive=True)
Fp,F=s.symbols('Fp F')
expr=C*(rho/eps)**(n-2)*(((rho/eps)**2-1)*Fp-2*(rho/eps)*F/eps)/(1+(rho/eps)**2)**(n-1)/eps**(n-2)
# asymptotic replacement: denominator (1+R^2)^(n-1) ~ R^(2n-2)
lead=s.powsimp(C*(rho/eps)**(n-2)*((rho/eps)**2*Fp-2*(rho/eps)*F/eps)/(rho/eps)**(2*n-2)/eps**(n-2),force=True)
assert s.simplify(lead-C*(rho**(2-n)*Fp-2*rho**(1-n)*F))==0
print('Leading scaled rim = C*(rho^(2-n) Fprime -2 rho^(1-n) F), before angular area normalization.')
