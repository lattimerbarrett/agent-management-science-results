import sympy as s
from pathlib import Path
b,x,y=s.symbols('b x y',real=True)
a,d=s.symbols('a d',positive=True)
I=s.I
# A constructive choice; A may be any real number in the boundary
# matrix calculation. For defining-function use choose A still larger
# and positive. Addition of 2 A |partial r|^2 preserves positivity.
A0=((x*x+y*y)/d-b+1)/(2*a*a)
H=s.Matrix([[b,x+I*y],[x-I*y,d]])
Hnew=H+s.diag(2*A0*a*a,0)
assert s.simplify(Hnew[0,0] - (1+(x*x+y*y)/d))==0
assert s.simplify(Hnew.det()-d)==0
# Sylvester: first diagonal = 1+(x²+y²)/d > 0, det=d>0.
v,w=s.symbols('v w',complex=True)
z=s.Matrix([v,w])
# Check completion of the square, giving positivity directly.
form=(s.conjugate(z).T*Hnew*z)[0]
square=d*(s.conjugate(w)+(x+I*y)*s.conjugate(v)/d)*(w+(x-I*y)*v/d)+s.conjugate(v)*v
assert s.simplify(s.expand(form-square))==0
# Verify defining-function modification Levi via real coordinates.
X,Y,U,V,A=s.symbols('X Y U V A',real=True)
r=s.Function('r')(X,Y,U,V)
coords=[(X,Y),(U,V)]
def dz(f,j):
    p,q=coords[j]; return (s.diff(f,p)-I*s.diff(f,q))/2
def dbar(f,j):
    p,q=coords[j]; return (s.diff(f,p)+I*s.diff(f,q))/2
for j in range(2):
    for k in range(2):
        lhs=dz(dbar(r+A*r*r,k),j)
        rhs=(1+2*A*r)*dz(dbar(r,k),j)+2*A*dz(r,j)*dbar(r,k)
        assert s.simplify(s.expand(lhs-rhs))==0

print("All exact symbolic checks passed.")
