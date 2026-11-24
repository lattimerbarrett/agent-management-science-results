import sympy as s
from pathlib import Path
S=s.diag(1,-1,1); E=s.diag(1,1,-1); R=s.diag(-1,-1,1)
phi=s.pi/4
Z=s.Matrix([[s.cos(phi),-s.sin(phi),0],[s.sin(phi),s.cos(phi),0],[0,0,1]])
T=Z*E
for O in [S,T]:
 assert s.simplify(O.T*O)==s.eye(3)
 assert s.simplify(O.det())==-1
 assert s.simplify(O*R-R*O)==s.zeros(3)
# O orthogonal,det-1 implies O reverses the sphere area via triple product.
a,b,c=s.symbols('a b c');v=s.Matrix([a,b,c])
assert S*s.Matrix([0,0,1])==s.Matrix([0,0,1])
assert T*s.Matrix([0,0,1])==s.Matrix([0,0,-1])
# Explicit phase equations for delta=pi/4,chi=pi/2.
# If phases match, s=m-3/8, t=9/8+2l; only m=1 permits s in[0,1].
assert [m for m in range(-3,4) if 0<=s.Rational(m)-s.Rational(3,8)<=1]==[1]
assert all(not(0<=s.Rational(9,8)+2*l<=1) for l in range(-5,6))
# Stronger uniform Euclidean separation bound in R6.
# Inner product sum=2 sin(theta)sin(eta)cos(A)cos(B),
# A in[-pi/8,7pi/8],B in[3pi/8,11pi/8].
# Maximum cos(A)cos(B) is cos(pi/8), so distance² >=4-4cos(pi/8).
d2=4-2*s.sqrt(2+s.sqrt(2))
assert d2.is_positive
print('Lagrangian graph matrices and halfturn invariance checked exactly.')
print('Arc-trace phase equations exclude intersection.')
print('Exact squared-distance lower bound:',d2,'approximately',s.N(d2,30))
# Bound exceeds 3/10: square exact inequalities if needed.
assert (d2-s.Rational(3,10)).is_positive
print('Thus trace separation exceeds sqrt(3/10), allowing disjoint support neighborhoods.')
Path('workspace/agent3_global_geometry_checks.py').write_text(Path('scratchpad.py').read_text())
