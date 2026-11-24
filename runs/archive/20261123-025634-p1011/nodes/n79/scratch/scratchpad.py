import sympy as s
r,n=s.symbols('r n', positive=True)
m=n-1
U=(1+r*r)**(-(n-2)/2)
b=(n-2)/(2*(n-1))
# On the boundary of the halfspace, the action density is
# D = |grad U|^2/2 - (n-2)^2 U^q/2.
D=(n-2)**2*s.Rational(1,2)*(r*r-1)*(1+r*r)**(-n)
U2=(1+r*r)**(-(n-2))
lapU2=s.diff(U2,r,2)+(m-1)/r*s.diff(U2,r)
print('First shape variation cancels:',s.simplify(s.powsimp(D-b*lapU2/2,force=True)))
# Spherical normalization and conformal Hessian.
a=4*(n-1)/(n-2); R=n*(n-1); q=2*n/(n-2)
print('Sphere action at constant 1:',s.simplify(R/2-R/q))
print('Interior Hessian potential divided by a:',s.simplify((R-R*(q-1))/a))
print('Sphere first shape variation:',s.simplify(R/n-m))
# For degree L, T=-(Delta+m) has eigenvalue (L-1)(L+n-1).
L=s.symbols('L',integer=True,nonnegative=True)
print('Boundary forcing eigenvalue:',s.factor(L*(L+n-2)-m))
print('Kernel dimensions: n tangent coordinate functions; constant mode negative, normal coordinate not Neumann.')
# Full joint Hessian is a A(v,v)+4 int(T f)v.
# Stationarity gives a A(v,v)=-2 int(T f)v, so reduced Hessian=-a A(v,v).
A,I=s.symbols('A I')
print('Reduced joint Hessian:',s.simplify((a*A+4*I).subs(I,-a*A/2)))
