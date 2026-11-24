import sympy as s
from scipy.integrate import quad
from math import pi
p,d=s.symbols('p d', positive=True)
a=(1-d)*(p-1)
Ap=s.simplify(1/(a+1)*(1/(1-a/(p-1)))**(p-1))
print('Scalar interval characteristic:', Ap)
print('Input integrand exponent:',s.simplify(p*(-1+d)+a))
F=1+1/(p*(p-1)); q=p/(p-1)
assert s.simplify(F-(1+1/(q*(q-1)))/(p-1))==0
print('Duality identity checked symbolically.')
for pv in [1.25,1.5,2,3,5]:
 for dv in [.2,.05,.01]:
  av=(1-dv)*(pv-1)
  characteristic=1/(av+1)*dv**(-(pv-1))
  # t=x*u; Hf(-x)= x^(d-1)/pi * integral_0^(1/x) u^(d-1)/(1+u) du.
  # Compare dimensionless integral with rigorous lower bound 1/(2*d).
  x=.1
  J=quad(lambda u:u**(dv-1)/(1+u),0,1/x,epsabs=1e-8)[0]
  assert J >= 1/(2*dv)
  print(f'p={pv:g}, delta={dv:g}, A_interval={characteristic:.8g}, delta*pi*Hf(-x)/x^(delta-1)={dv*J:.8g}')
open('workspace/agent1_scalar_checks.py','w').write(open('scratchpad.py').read())
