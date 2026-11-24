import sympy as s
from pathlib import Path
D=s.Integer(15);m=s.Integer(31);z=s.symbols('z')
g0=(s.gamma(s.Rational(3,2))/s.gamma(D+s.Rational(1,2)))**2
g1=(s.gamma(2)/s.gamma(D+1))**2
A=s.simplify((g0+g1)/(D-1))
B=s.simplify((g0*(2*D**2+D+8)+g1*(6*D**2+3*D+2))/((D-2)*(D-1)*(2*D+1)))
C=s.simplify((g0*(4*D**4+165*D**2-41*D+114)+g1*(36*D**4+181*D**2+19*D+6))/((D-3)*(D-2)*(D-1)*(2*D+1)**2))
b=s.factor(B/A);c=s.factor(C/A)
q3=(m*b-m-4)/2;qt=2*(1+b)/m
p=1-4*b*z+3*c*z*z
lo=s.Rational(3616,10000);hi=s.Rational(3617,10000)
assert p.subs(z,lo)>0 and p.subs(z,hi)<0
assert s.diff(p,z).subs(z,hi)<0
print('smaller scale root certified in',lo,hi)
for ai2 in [0,1]:
 h=4*z*(-1+z*b)*(2+4*ai2)/(m*(m+2))+z*z*(q3*(16/(m*(m+2)*(m+4))+16*ai2/((m+2)**2*(m+4)))+qt*(4*(m+4)**2*ai2/(m*(m+2)**2)))
 hz=s.Poly(s.cancel(h/z),z)
 assert hz.degree()==1
 assert hz.eval(lo)<0 and hz.eval(hi)<0
 print('Exact negative translation coefficient certified for ai^2=',ai2,' root interval; value approx',float(h.subs(z,(lo+hi)/2)))
print('Full n32 finite-dimensional nondegenerate minimum verified (given Hessian reduction).')
