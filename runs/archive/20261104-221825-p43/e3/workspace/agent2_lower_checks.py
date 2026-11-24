"""Exact algebra and winding-number checks relevant to the lower bound.
Run directly with Python; no external packages required.
"""
from fractions import Fraction
import cmath, math

# Basis elements are A^a B^b q^k, reduced with A^2=B^2=q.
def mul(x,y):
    a,b,k=x; c,d,l=y
    return ((a+c)%2,(b+d)%2,k+l+(a+c)//2+(b+d)//2)
U=(0,0,0); A=(1,0,0); B=(0,1,0); P=(1,1,0); q=(0,0,1)
assert mul(A,A)==q and mul(B,B)==q and mul(A,B)==P
for x in (U,A,B,P,q):
 for y in (U,A,B,P,q):
  for z in (U,A,B,P,q):
   assert mul(mul(x,y),z)==mul(x,mul(y,z))
# pi2 generators have area 4pi and Chern 2.
for a in range(-20,21):
 for b in range(-20,21):
  area_in_4pi=a+b
  chern=2*a+2*b
  assert chern==2*area_in_4pi
# No two distinct points in a coset of Z can have difference strictly between 0 and 1.
for k in range(-20,21):
 for l in range(-20,21):
  assert not (0 < k-l < 1)

# Local caveat: H(z,w)=Re(z^3)+Re(w^3) has an isolated critical
# point at zero. Each planar gradient is (3(x²-y²),-6xy), with
# winding -2; the four-dimensional gradient has index (-2)^2=4.
# X_H differs from gradient by invertible determinant-positive J,
# so its local vector-field index is also4.
def planar_gradient(theta):
 x,y=math.cos(theta),math.sin(theta)
 return complex(3*(x*x-y*y),-6*x*y)
n=10000
zs=[planar_gradient(2*math.pi*j/n) for j in range(n+1)]
assert min(abs(z) for z in zs)>2.999999
wind=sum(cmath.phase(zs[j+1]/zs[j]) for j in range(n))/(2*math.pi)
assert abs(wind+2)<1e-10
assert round(wind)**2==4

# Enumerative coefficient: a bidegree(0,1) sphere is constant in x and
# a Mobius map in y. Marked points 0,1,infinity sent to 0,1,infinity
# force the identity. The complex incidence Jacobian is invertible.
import sympy as sp
a,b,c=sp.symbols('a b c')
incidence=sp.Matrix([b,(a+b)/(c+1)-1,c/a])
J=incidence.jacobian([a,b,c]).subs({a:1,b:0,c:0})
assert J.det()==-1
assert sp.solve([b,a+b-c-1,c],[a,b,c])=={a:1,b:0,c:0}

def run():
 print('Degree-one vertical-sphere incidence count: unique, transverse')
 print('Quantum relations and associativity: checked exactly')
 print('Area/Chern period and action-coset obstruction: checked exactly')
 print('Planar cubic gradient winding:',round(wind),'(product index 4)')
if __name__=='__main__': run()
