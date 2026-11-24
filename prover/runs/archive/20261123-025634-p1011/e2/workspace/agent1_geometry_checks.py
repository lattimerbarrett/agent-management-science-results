import sympy as s
from pathlib import Path
n,t=s.symbols('n t', positive=True)
m=(n-2)/2
c=(n-2)/(4*(n-1))
# U=(1+|x'|^2)^(-m) at the flat boundary, q=2n/(n-2).
# Radial Laplacian in d=n-1 dimensions on functions of t=|x'|^2.
# For U^2=(1+t)^(-(n-2)), Delta'=4t d_tt +2(n-1)d_t.
f=(1+t)**(-(n-2))
lap=s.diff(f,t,2)*4*t+s.diff(f,t)*2*(n-1)
grad2=(n-2)**2*t*(1+t)**(-n)
Uq=(1+t)**(-n)
# Divide all terms by positive common factor (1+t)^(-n).
lap_scaled=s.simplify(s.expand_power_base(lap*(1+t)**n, force=True))
res=s.simplify(-(n-2)**2*t/2+(n-2)**2/2+c*lap_scaled)
assert res==0, res
print('General symbolic boundary shape first-variation cancellation:',res)
# Principal curvatures of ellipsoid at (a1,0,...,0).
a1,a2,a3=s.symbols('a1 a2 a3',positive=True)
x2,x3=s.symbols('x2 x3',real=True)
phi=a1*s.sqrt(1-x2*x2/a2**2-x3*x3/a3**2)
assert s.diff(phi,x2,2).subs({x2:0,x3:0})==-a1/a2**2
assert s.diff(phi,x3,2).subs({x2:0,x3:0})==-a1/a3**2
print('Ellipsoid curvatures at axial point:',a1/a2**2,a1/a3**2)
# Strict convexity follows Hess F positive definite for F=sum x_j^2/a_j^2-1.
# Quantitative boundary Poincare estimate derives from n int(v^2)=int_boundary (x.nu)v^2-2 int v x.grad v.
# Verify scalar Young inequality used with a=||v||, b=||grad v||:
a,b,R=s.symbols('a b R',nonnegative=True)
young=s.factor(n*a*a/2+2*R*R*b*b/n-2*R*a*b)
assert s.simplify(young-(n*a-2*R*b)**2/(2*n))==0
print('Boundary Poincare Young remainder:',young)
