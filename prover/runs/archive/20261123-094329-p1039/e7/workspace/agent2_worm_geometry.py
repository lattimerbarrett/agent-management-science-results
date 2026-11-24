import sympy as s
# Exact scalar verification of pseudoconvex worm geometry.
# No assertion concerning the Oka property is encoded here.
x,y,h,p,q=s.symbols('x y h p q', real=True)
z,zb,t=s.symbols('z zb t')
eta_fun=s.Function('eta')(t)
rho=z*zb-z*s.exp(-s.I*t)-zb*s.exp(s.I*t)+eta_fun
rho_z=s.diff(rho,z)
rho_t=s.diff(rho,t)
assert s.simplify(s.diff(rho_z,zb)-1)==0
assert s.simplify(s.diff(rho_z,t)-s.I*s.exp(-s.I*t))==0
assert s.simplify(s.diff(rho_t,t)-(z*s.exp(-s.I*t)+zb*s.exp(s.I*t)+s.diff(eta_fun,t,2)))==0
# Multiply tangent Levi form by |w|² and rotate z*exp(-it)=x+iy.
grad_z_norm=(x-1)**2+y*y
grad_w_scaled=p-2*y
cross=2*y*(p-2*y)
raw=grad_w_scaled**2+(2*x+q)*grad_z_norm+cross
L=p*p-2*p*y+(2*x+q)*(1-h)
assert s.factor(raw-L)==(2*x+q)*(h+x*x-2*x+y*y)
# On boundary, 2x=x²+y²+h. Therefore L equals the following sum.
completed=(1-h)*(y-p/(1-h))**2 + (1-h)*x*x + h*(1-h)+(1-h)*q-h*p*p/(1-h)
assert s.factor(L-completed)==(h-1)*(h+x*x-2*x+y*y)
# For 0<=h<=1/3, q>=h*p²/(1-h)² proves nonnegativity.
# Explicit cutoff h=e^8 exp(-1/s), 0<s<=1/8 on relevant boundary.
a=s.symbols('a', positive=True)
eta=s.exp(8-1/a)
eta1=s.diff(eta,a)
eta2=s.diff(eta1,a)
assert s.simplify(eta1-eta/a**2)==0
assert s.simplify(eta2-eta*(1-2*a)/a**4)==0
# q/p²=(1-2a)/h >= (3/4)/h for a<=1/8.
# For h<=1/3 this is >= h/(1-h)², because 3(1-h)²-4h²>=0.
poly=s.expand(3*(1-h)**2-4*h*h)
assert poly==3-6*h-h*h
assert poly.subs(h,s.Rational(1,3))==s.Rational(8,9)
assert s.diff(poly,h)==-6-2*h
# For h>=1/3, eta2>=h*(3/4)/(1/8)^4 >=1024 >1.
assert s.Rational(1,3)*s.Rational(3,4)*8**4==1024
# If q>=1, use boundary y²<=1-h and x>=0:
# L=(p-y)² +(2x+q)(1-h)-y² >= (p-y)².
assert s.expand(L-((p-y)**2+(2*x+q)*(1-h)-y*y))==0
# Grad rho can vanish only if z=e^{it}, eta'=0. Boundary there eta=1,
# but explicit cutoff derivative at eta=1 (a=1/8) is 64, nonzero.
assert eta.subs(a,s.Rational(1,8))==1
assert eta1.subs(a,s.Rational(1,8))==64
print('Verified exact scalar Levi inequalities for explicit smooth pseudoconvex worm.')
print('Smoothness/connectedness follow from disc fibers; no non-Oka result proved.')
