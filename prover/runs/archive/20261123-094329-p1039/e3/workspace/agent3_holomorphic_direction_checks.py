import sympy as s
from pathlib import Path
eps=s.Rational(1,100)
k=s.sqrt(2*eps)
assert k<s.Rational(1,7)
M=s.simplify((1+k)/(1-k))
assert M<s.Rational(4,3)
# Exact boundary error after replacing k by 1/7, M by 4/3.
assert s.sqrt(1+s.Rational(16,9))/7==s.Rational(5,21)
assert s.Rational(5,21)<1
theta=s.symbols('theta', real=True)
z=s.exp(s.I*theta)
assert s.integrate(s.conjugate(z)*s.diff(z,theta),(theta,0,2*s.pi))==2*s.pi*s.I
text='''No holomorphic quadratic line-escape choice for a smooth ball family. Let g(z)=(1,z), R(z)^2=(99/100)(1+|z|^2) for |z|<=1. There is no holomorphic map b from a neighborhood of the closed unit disc to C^2 minus {0} such that the affine line g(z)+C b(z) avoids the closed radius-R(z) ball for every z. Indeed that condition implies |b1+bar(z)b2|^2 < (1/100)(1+|z|^2)(|b1|^2+|b2|^2), by the formula for distance from 0 to a complex line. If b2 vanished, it would imply 1<(1/100)(1+|z|^2)<=1/50. Hence h=b1/b2 is holomorphic. On the unit circle, |h+bar z|<k sqrt(|h|^2+1), k=sqrt(1/50)<1/7. Using |h|-1<=|h+bar z| and sqrt(|h|^2+1)<=|h|+1 gives |h|<(1+k)/(1-k)<4/3, hence |h+bar z|<5/21. But Cauchy's theorem gives integral (h+bar z) dz=2pi i, forcing its supremum modulus on that circle >=1. Contradiction. This rules out a naive holomorphic family of quadratic polynomial curves; it does NOT rule out transcendental FB families or Oka property.\n'''
Path('workspace/agent3_holomorphic_direction_obstruction.txt').write_text(text)
print('PASS exact constants and boundary Fourier integral')
print(text)
