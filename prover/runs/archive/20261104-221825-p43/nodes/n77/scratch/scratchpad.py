import sympy as s
from scipy.optimize import differential_evolution
from math import pi, cos, sin, sqrt
# Examine the spectral-invariant bound furnished by A*A=q[M].
# With sphere area P, it forces a-P < b < a.
P=s.symbols('P', positive=True)
a=0; b=-P/2
print('Two action cosets satisfy both strict inequalities:',s.simplify(a-b),s.simplify(b-(a-P)))
# Separation of the two swept Lagrangian hemispheres in the proposed construction.
f=lambda z: -(cos(z[0]+z[1]+pi/4)+sin(z[0]-z[1]))
r=differential_evolution(f,[(0,pi),(0,pi)],tol=1e-12,seed=1)
print('Maximum total dot product:',-r.fun)
print('Predicted maximum:',sqrt(2+sqrt(2)))
print('Squared separation lower bound:',4-2*sqrt(2+sqrt(2)))
# Longitude estimate: for g>=0, g<=1, g'<=0, and 0<=w<=r,
# g+r*g' <= g+g'*w <= g <=1.
r0,w=s.symbols('r w', nonnegative=True); gp=s.symbols('gp', nonpositive=True)
print('Longitude-bound differences:',s.expand((gp*w)-(gp*r0)),s.expand(-gp*w))
