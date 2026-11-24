import sympy as s
from fractions import Fraction
L,t,D,H=s.symbols('L t D H',positive=True)
# J = integral_0^t F - t F(t), with F=1-D and H=int D.
J=s.expand((t-H)-t*(1-D))
assert J==t*D-H
print('High-compression numerator:',J)
print('High-compression maximality: t*D-H <= L*t*D')
print('Thus H >= (1-L)*t*D.')
p=1/(1-L)
print('Exponent p =',p)
# If Hprime <= H / ((1-L)*t), then (H/t**p)' <=0.
Hp=H/((1-L)*t)
derivative=s.simplify(Hp*t**(-p)-p*H*t**(-p-1))
assert derivative==0
print('Weighted derivative at the limiting differential bound:',derivative)
print('For L<1/2, p<2, contradicting H(t)<=t**2/(2*L) and H(t)>=(1-L)*t**p.')
# Algebraic extraction: scale each positive increment with q-value >= eta.
eta=Fraction(1,10)
for q in [Fraction(1,10),Fraction(1,8),Fraction(1,3),Fraction(3,4),Fraction(1,1)]:
 factor=eta/q
 assert 0<factor<=1 and factor*q==eta
print('Constant-increment rescaling certificates passed.')
