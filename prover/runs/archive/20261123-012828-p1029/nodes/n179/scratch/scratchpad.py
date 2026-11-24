import sympy as s
C=s.symbols('C', positive=True)
m=s.symbols('m', integer=True, positive=True)
Cp=C/(m-(m-1)*C)
f=lambda z:1-1/z
print('Join-recurrence slack:',s.factor(f(Cp)-m*f(C)))
eta,t=s.symbols('eta t',positive=True)
delta=(eta-t)/(1-t)
print('Spectral dimension threshold:',delta)
print('Scalar-model slack, C=1/t:',s.factor((1-t)-delta))
from fractions import Fraction as F
count=0
for q in range(2,101):
 for p in range(1,q//2+1):
  e=F(p,q)
  for k in range(1,10):
   u=e*F(k,10)
   d=(e-u)/(1-u)
   assert 0<d<=1-u
   count+=1
print('Exact admissible threshold checks:',count)
