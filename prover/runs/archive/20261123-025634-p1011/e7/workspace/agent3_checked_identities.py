import sympy as s
r,a,b,n=s.symbols('r a b n', positive=True)
v=a*r**(2-n)+b
vr=s.diff(v,r)
P=s.factor(r**(n-1)*((n-2)*v*vr/2+r*vr**2/2))
assert s.simplify(P+(n-2)**2*a*b/2)==0
print('Harmonic radial Pohozaev density / unit spherical area:',P)
for N in range(3,7):
    val=s.simplify(P.subs(n,N))
    print('n=',N,'P/hemisphere_area=',val)
# radial standard bubble: critical Pohozaev invariant must vanish
for N in range(3,11):
    U=(1+r*r)**(-s.Rational(N-2,2))
    Ur=s.diff(U,r)
    density=(N-2)*U*Ur/2 +r*Ur**2/2 +s.Rational((N-2)**2,2)*r*(1+r*r)**(-N)
    assert s.simplify(density)==0
print('Radial critical-bubble Pohozaev verified for n=3,...,10')
# exact conformal Robin transformation: ghat=e^(2w)g, u=e^(-(n-2)w/2)v
w,dw,v,dv,H=s.symbols('w dw v dv H')
m=(n-2)/2
c=(n-2)/(4*(n-1))
# hatted normal derivative plus Robin expressed after factoring exp(-n*w/2)
Bhat=dv-m*dw*v+2*c*(H+(n-1)*dw)*v
assert s.simplify(Bhat-(dv+2*c*H*v))==0
print('Robin conformal covariance algebra verified in symbolic n')
# n=3: first nonumbilic Green correction for a tracefree quadratic graph
x,y,t,aa,bb=s.symbols('x y t aa bb', real=True)
rho=s.sqrt(x*x+y*y+t*t)
f=aa*(x*x-y*y)/2+bb*x*y
q=f/(2*(rho+t)**2)
lapq=s.simplify(sum(s.diff(q,z,2) for z in (x,y,t)))
assert lapq==0
qt0=s.simplify(s.diff(q,t).subs(t,0))
assert s.simplify(qt0+f/(x*x+y*y)**s.Rational(3,2))==0
# Homogeneous degree zero, so no radial derivative; its spherical average vanishes
assert s.simplify(sum(z*s.diff(q,z) for z in (x,y,t)))==0
print('n=3 angular Green correction q=f/[2(r+t)^2]: harmonic, correct Neumann datum, degree zero')
# Explicit angular cancellation in halfspace ADM mass and flattening gauge
phi,theta,R=s.symbols('phi theta R', real=True, positive=True)
q_sphere=s.simplify(q.subs({x:s.sin(theta)*s.cos(phi),y:s.sin(theta)*s.sin(phi),t:s.cos(theta)}, simultaneous=True))
# replace rho=1, valid for 0<=theta<=pi/2
q_sphere=s.sin(theta)**2*(aa*s.cos(2*phi)+bb*s.sin(2*phi))/(4*(1+s.cos(theta))**2)
assert s.integrate(q_sphere,(phi,0,2*s.pi))==0
F=aa*s.cos(2*phi)/2+bb*s.sin(2*phi)/2
assert s.integrate(F,(phi,0,2*s.pi))==0
assert s.integrate(s.diff(F,phi,2),(phi,0,2*s.pi))==0
print('n=3 angular Green and boundary-flattening mass terms average to zero')
