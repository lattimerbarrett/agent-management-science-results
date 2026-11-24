from fractions import Fraction
import sympy as s
# Audit the scalar distribution forced by a putative half-absorption pair.
def F(t): return max(Fraction(0),1-t)
N=60
count=0
for i in range(1,2*N+1):
 for j in range(1,2*N+1):
  u,v=Fraction(i,N),Fraction(j,N)
  assert 2*F((u+v)/2)<=F(u)+F(v)
  count+=1
t=s.symbols('t',real=True)
print('Uniform survival function passes',count,'exact midpoint-convexity tests.')
print('Integral on [0,1]:',s.integrate(1-t,(t,0,1)))
print('Moments:',[s.integrate(t**k,(t,0,1)) for k in range(1,6)])