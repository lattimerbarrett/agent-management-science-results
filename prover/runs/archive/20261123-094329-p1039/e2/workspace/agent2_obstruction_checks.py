"""Exact checks ruling out two tempting but invalid non-Oka obstructions.
These computations prove NO existence claim in the main problem.
"""
from fractions import Fraction as Q
import sympy as s

# Holomorphic C* meridian avoiding a fixed logarithmic torus neighborhood.
r, theta = s.symbols('r theta', positive=True, real=True)
zeta = r*(s.cos(theta)+s.I*s.sin(theta))
h1 = zeta + 1/zeta
h2 = -s.I*(zeta - 1/zeta)
u = s.simplify(s.expand_complex(s.re(h1)))
v = s.simplify(s.expand_complex(s.re(h2)))
assert s.trigsimp(u-(r+1/r)*s.cos(theta)) == 0
assert s.trigsimp(v-(r+1/r)*s.sin(theta)) == 0
assert s.trigsimp(u*u+v*v-(r+1/r)**2) == 0
assert s.factor((r+1/r)**2-4) == (r-1)**2*(r+1)**2/r**2
# Therefore (exp(h1), exp(h2)) stays outside log-radius 2, winding +1.

# Uniform Hénon escape of a VERY THIN solid circle tube.
a, M, delta = Q(1,10), Q(10**6), Q(1,10**8)
zlo,zhi=Q(9,10),Q(11,10)
w1lo=a*zlo-M*delta**2
w1hi=a*zhi+M*delta**2
w2lo=M*w1lo**2-a*delta
assert w1lo>0 and w2lo>8000 and w2lo>w1hi
# In cone |w|>=max(|z|,2), H(z,w)=(w,az+Mw²) remains in cone
# and doubles |w| by the reverse triangle inequality.
assert M*2-a>2
print('Exact checks passed: exponential meridian and uniform thin-tube Henon escape.')
