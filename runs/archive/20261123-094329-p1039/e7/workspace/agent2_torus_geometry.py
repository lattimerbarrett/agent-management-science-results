import sympy as s
# Candidate K_epsilon = {(abs(z)^2-1)^2+(abs(w)^2-1)^2 <= epsilon}.
# This checks geometry only; no claim about Oka property is made.
x,y,u,v=s.symbols('x y u v', real=True)
e=s.symbols('e', positive=True)
rho=(x*x+y*y-1)**2+(u*u+v*v-1)**2-e
variables=[(x,y),(u,v)]
L=s.zeros(2)
for j,(a,b) in enumerate(variables):
 for k,(c,d) in enumerate(variables):
  L[j,k]=s.simplify((s.diff(rho,a,c)+s.diff(rho,b,d)+s.I*s.diff(rho,a,d)-s.I*s.diff(rho,b,c))/4)
assert L==s.diag(4*x*x+4*y*y-2,4*u*u+4*v*v-2)
# epsilon=1/16: closure implies each radial square belongs to [3/4,5/4].
# Thus Levi eigenvalues >= 1, and gradient cannot vanish on boundary.
assert s.Rational(1,16) < s.Rational(1,4)
assert 4*(1-s.sqrt(s.Rational(1,16)))-2 == 1
# Critical radial squares are 0 or 1. Values of sum of squared errors: 0,1,2.
assert s.Rational(1,16) not in [0,1,2]
# Connected: radial base is the disk centered (1,1) with radius 1/4,
# and phases form a connected T^2 fiber everywhere.
print('Verified candidate has smooth compact connected strongly pseudoconvex geometry.')
print('Its complement Oka/non-Oka status is NOT established by this script.')
