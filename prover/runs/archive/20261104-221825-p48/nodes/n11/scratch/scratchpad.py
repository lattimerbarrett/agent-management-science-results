import sympy as s
# Vertical Levi of phi(v)=1/(|v1|^2+|v2|^2).
# At v=(r,0), its radial and angular eigenvalues are r^(-4), -r^(-4).
r=s.symbols('r', positive=True)
t=s.symbols('t', positive=True)
f=1/t
radial=s.simplify(s.diff(f,t)+t*s.diff(f,t,2))
angular=s.diff(f,t)
print('radial eigenvalue:',radial.subs(t,r*r))
print('angular eigenvalue:',angular.subs(t,r*r))
# Useful polarization data for the degeneration.
e=s.symbols('e',integer=True,nonnegative=True)
def dot(x,y):
 a,b=x;c,d=y
 return s.expand(-e*a*c+a*d+b*c)
H=(1,3*e+1);D=(1,-2*e-1)
print('H^2 =',dot(H,H))
print('H.D =',dot(H,D))
print('D^2 =',dot(D,D))
print('Split summands = 2H +/- 3D:',tuple(s.expand(2*H[i]+3*D[i]) for i in range(2)),tuple(s.expand(2*H[i]-3*D[i]) for i in range(2)))
