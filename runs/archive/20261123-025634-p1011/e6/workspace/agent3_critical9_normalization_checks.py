import sympy as s
from pathlib import Path
q=s.symbols('q',positive=True)
# Apply only Gamma(z+1)=z Gamma(z), keeping base gamma values symbolic.
g7,g8=s.symbols('g7 g8',positive=True)
g9=(q+7)*g7/2;g10=(q+8)*g8/2
Cspec=2**19*g10**2/g7**2
c=-s.Rational(8,17)*(q+7)*(q+8)
Dcrit=2*g9**2/g8**2
ratio=s.factor(Cspec/(c*c/Dcrit))
assert ratio==2**10*17**2
print('All-q exact spectral/physical critical-log ratio:',ratio)
# Leading homogeneous source coefficient, n=18,d=9.
source=s.factor(16*((1-9)+(9*(9+18-3)-q*(q+18-3))/s.Integer(34)))
assert s.simplify(source-c)==0
print('Critical source coefficient:',source)
