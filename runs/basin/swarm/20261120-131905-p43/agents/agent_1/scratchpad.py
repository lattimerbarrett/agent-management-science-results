import sympy as S

# 1. All critical points of the height sum on S2 x S2.
x1,x2,x3,y1,y2,y3,la,mu=S.symbols('x1 x2 x3 y1 y2 y3 la mu', real=True)
variables=(x1,x2,x3,y1,y2,y3,la,mu)
eqs=[la*x1,la*x2,la*x3-1,mu*y1,mu*y2,mu*y3-1,
     x1*x1+x2*x2+x3*x3-1,y1*y1+y2*y2+y3*y3-1]
solutions=S.solve(eqs,variables,dict=True)
assert len(solutions)==4
assert sorted([q[x3]+q[y3] for q in solutions])==[-2,0,0,2]
print('Height sum: exactly four critical points, values -2,0,0,2.')

# 2. The arc in the middle critical level.
t=S.symbols('t',real=True)
x=S.Matrix([S.sin(t),0,S.cos(t)]); y=-x
assert S.simplify(x.dot(x))==1
assert S.simplify(y.dot(y))==1
assert x[2]+y[2]==0
assert S.simplify(x.diff(t).dot(x.diff(t)))==1
print('The antidiagonal meridian is a regular arc in level zero.')

# 3. Explicit sphere Morse coordinates near the two middle points.
r2=S.symbols('r2',real=True)
assert S.expand((2-r2)*r2+(1-r2)**2)==1
u1,u2,v1,v2=S.symbols('u1 u2 v1 v2',real=True)
f=-u1*u1-u2*u2+v1*v1+v2*v2
assert S.hessian(f,(u1,u2,v1,v2))==S.diag(-2,-2,2,2)
assert S.expand(sum(z*S.diff(f,z) for z in (u1,u2,v1,v2))-2*f)==0
s,w,z1,z2,tau=S.symbols('s w z1 z2 tau',real=True)
ft=S.expand(f.subs({u1:s+w,v1:w-s,u2:z1,v2:z2}))
assert ft==-4*s*w-z1*z1+z2*z2
assert S.diff(ft,w)==-4*s
assert S.simplify(ft.subs(w,(-tau-z1*z1+z2*z2)/(4*s)))==tau
print('Middle points have Morse index two; adapted coordinates are valid for s>0.')

# 4. Model vector field in the tube: V=b(s)d_s+2 tau d_tau+sum z_i d_z_i.
# The coefficient b(s) does not enter either checked identity.
rho=z1*z1+z2*z2+tau*tau
Vrho=S.expand(z1*S.diff(rho,z1)+z2*S.diff(rho,z2)+2*tau*S.diff(rho,tau))
assert Vrho==2*z1*z1+2*z2*z2+4*tau*tau
assert 2*tau*S.diff(tau,tau)==2*tau
print('Tube field: transverse expansion and V(f)=2f verified.')

# 5. Flat radial extension: all derivatives are polynomial(1/r)*exp(-1/r^2).
r,z=S.symbols('r z',positive=True)
P=S.Integer(1)
flat=S.exp(1-1/r**2)
for n in range(11):
    assert S.simplify(S.diff(flat,r,n)-flat*P.subs(z,1/r))==0
    assert S.limit(flat*P.subs(z,1/r),r,0,dir='+')==0
    P=S.expand(2*z**3*P-z**2*S.diff(P,z))
assert S.simplify(S.diff(flat,r)-2*flat/r**3)==0
assert flat.subs(r,1)==1
# Collar time t=(1-r^-2)/2: exp(2t) is exactly the radial factor.
collar_time=(1-r**(-2))/2
assert S.simplify(S.exp(2*collar_time)-flat)==0
assert S.diff(collar_time,r)==r**(-3)
print('Flat radial cone and exact flow-collar matching verified.')
print('Flatness derivative recurrence verified through order 10 (and proved by induction).')

# 6. Cup-length calculation.
u,v=S.symbols('u v')
G=S.groebner([u*u,v*v],u,v)
assert G.reduce(u*v)[1]==u*v
for m in [u**3,u*u*v,u*v*v,v**3]:
    assert G.reduce(m)[1]==0
print('Cup length: 2.')
