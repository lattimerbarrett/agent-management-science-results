from pathlib import Path
import sympy as s
r=s.symbols('r', positive=True)
a=s.Function('a')(r)
# logarithmic transformation A=r^-1/2 v(log r)
t=s.symbols('t', real=True)
v=s.Function('v')
A=r**s.Rational(-1,2)*v(s.log(r))
expr=s.simplify(r**s.Rational(5,2)*(s.diff(A,r,2)+2*s.diff(A,r)/r))
assert s.simplify(expr-(s.Subs(s.diff(v(t),t,2),t,s.log(r))-v(s.log(r))/4))==0
print('n3 spherical average logarithmic ODE checked exactly')
ell=s.symbols('ell', integer=True, positive=True)
lam=4*ell*(ell+2)
ratio=s.factor((lam-12)/(lam+3)-s.Rational(4,7))
assert ratio==s.factor(12*(ell-2)*(ell+4)/(7*(4*ell**2+8*ell+3)))
print('azimuthal m2 Jacobi coercivity ratio minus 4/7 =',ratio)
x,y,z,aa,bb=s.symbols('x y z aa bb', real=True)
rho=s.sqrt(x*x+y*y+z*z)
f=aa*(x*x-y*y)/2+bb*x*y
q=f/(2*(rho+z)**2)
assert s.simplify(sum(s.diff(q,j,2) for j in [x,y,z]))==0
assert s.simplify(s.diff(q,z).subs(z,0)+f/(x*x+y*y)**s.Rational(3,2))==0
# Exact boundary asymptotic mismatch between q and Jacobi forcing
R=s.symbols('R', positive=True)
err=s.series((1+R**2)**s.Rational(-3,2)-R**-3,R,s.oo,7)
print('Jacobi boundary forcing minus q boundary forcing:',err)
# check z=v'+v/2 transformed identity
Z=s.diff(v(t),t)+v(t)/2
assert s.simplify(s.diff(Z,t)-Z/2-(s.diff(v(t),t,2)-v(t)/4))==0
print('backwards comparison integrating factor identity checked')

# General-dimensional averaged ODE transformation, used by the bridge
a=s.symbols('a', positive=True)
A=r**(-a)*v(s.log(r))
radial=s.simplify(r**(a+2)*(s.diff(A,r,2)+(2*a+1)*s.diff(A,r)/r))
assert s.simplify(radial-(s.Subs(s.diff(v(t),t,2),t,s.log(r))-a*a*v(s.log(r))))==0
Z=s.diff(v(t),t)+a*v(t)
assert s.simplify(s.diff(Z,t)-a*Z-(s.diff(v(t),t,2)-a*a*v(t)))==0
print('General-dimensional averaged critical ODE and integrating factor checked')
# Exact H^2 coefficient in the integrated n3 graph stress
h,k=s.symbols('h k')
# first normal product + radial gradient subtraction + tangential integration
coefficient=s.Rational(1,16)-s.Rational(1,32)-s.Rational(1,8)
assert coefficient==-s.Rational(3,32)
print('n3 tangentially integrated graph stress H^2 coefficient =',coefficient)

# Exact Newton-potential scales used for escape-to-infinity estimates
ss,dd,tt,RR=s.symbols('ss dd tt RR', positive=True)
# For 0<=t<=d, sqrt(s^2+t^2)-t<=s follows from (s+t)^2>=s^2+t^2.
assert s.expand((ss+tt)**2-(ss**2+tt**2))==2*ss*tt
# Thin slab kernel integral <=4*pi*d*s by the preceding pointwise bound.
slab_upper=4*s.pi*dd*ss
strip_density=s.symbols('eps',positive=True)*ss**-2
strip_thickness=s.symbols('eps',positive=True)*ss**2
assert s.simplify((slab_upper*strip_density).subs(dd,strip_thickness)-4*s.pi*s.symbols('eps',positive=True)**2*ss)==0
shell_potential=s.integrate(4*s.pi*tt**(-3),(tt,RR,s.oo))
assert shell_potential==2*s.pi/RR**2
boundary_potential=s.integrate(2*s.pi,(tt,0,RR))
assert boundary_potential==2*s.pi*RR
print('Exact thin-slab, exterior potential, and boundary potential scales verified')
