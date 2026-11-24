import sympy as s
from pathlib import Path
n,j,r=s.symbols('n j r', positive=True)
# Coefficient identity for harmonic degree-two P times r^(2j).
first=j*(2*j+n+1)/(n-1)
second=s.factor(first-(2*j+1))
assert s.simplify(second-(2*j*j+(3-n)*j-n+1)/(n-1))==0
# Pfaff-Saalschutz finite-sum beta coefficient, validated independently by
# exact integration for integer alpha, degrees j and k (no numerical claim).
t=s.symbols('t')
count=0
for a in [3,4,5,6]:
 for J in range(min(3,a-1)):
  for k in range(7):
   # use integer alpha-1/2 instead for exact polynomial integration:
   alpha=s.Rational(2*a+1,2)
   C=s.gegenbauer(k,alpha,t)
   direct=s.integrate(s.expand((1-t*t)**a*C*(1+t)**J/(1-t)**(J+1)),(t,-1,1))
   formula=0
   for p in range(J+1):
    q=J+1-p
    I=2**(2*alpha-q)*s.beta(alpha+s.Rational(1,2)-q,alpha+s.Rational(1,2))*s.rf(2*alpha,k)*s.rf(q,k)/(s.factorial(k)*s.rf(2*alpha+1-q,k))
    formula+=s.binomial(J,p)*2**(J-p)*(-1)**p*I
   formula=s.expand_func(formula)
   assert s.simplify(direct-formula)==0,(alpha,J,k,direct,formula)
   count+=1
print('Verified',count,'exact Gegenbauer-beta coefficients and all-symbolic radial source identity.')
