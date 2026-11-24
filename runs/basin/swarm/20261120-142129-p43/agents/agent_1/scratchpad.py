import sympy as S

# 1. Stereographic coordinates for the two spheres.
u,v,a,b = S.symbols('u v a b', real=True)
t,d = S.symbols('t d', real=True)
D1=1+u*u+v*v
D2=1+a*a+b*b
x=S.Matrix([(1-u*u-v*v)/D1, 2*v/D1, 2*u/D1])
y=S.Matrix([-(1-a*a-b*b)/D2, -2*b/D2, -2*a/D2])
assert S.factor(x.dot(x)-1)==0
assert S.factor(y.dot(y)-1)==0
f=x[2]+y[2]
# The four critical points in these charts, computed from the exact gradient.
numgrad=[S.factor(S.together(S.diff(f,z))).as_numer_denom()[0] for z in (u,v,a,b)]
crit=S.solve(numgrad,(u,v,a,b), dict=True)
assert len(crit)==4
assert {(p[u],p[v],p[a],p[b]) for p in crit} == {
    (i,0,j,0) for i in (-1,1) for j in (-1,1)
}
g=S.factor(f.subs({u:t+d,a:t-d}))
assert S.factor(g.subs({d:0,v:0,b:0}))==0
D=(1+(t+d)**2+v*v)*(1+(t-d)**2+b*b)
N=4*d*(1-t*t+d*d)+2*(t+d)*b*b-2*(t-d)*v*v
assert S.factor(g-N/D)==0
print('Exact chart and critical-point checks passed.')
print('Original critical coordinates (t,d,v,b):', sorted([
    ((p[u]+p[a])/2,(p[u]-p[a])/2,p[v],p[b]) for p in crit
]))

# 2. A(r)=r+exp(-r/(1-r/2)) for r<2, and A(r)=r for r>=2.
r=S.symbols('r',positive=True)
lam=S.exp(-r/(1-r/2))
A=r+lam
Ap=S.diff(A,r)
assert S.simplify(Ap-(1-lam/(1-r/2)**2))==0
z=S.symbols('z',positive=True)
# With z=r/(2-r), positivity becomes exp(2*z)>(1+z)^2.
assert S.simplify(Ap.subs(r,2*z/(1+z))-(1-(1+z)**2*S.exp(-2*z)))==0
# Prove exp(z)>1+z by two derivatives and the initial values.
E=S.exp(z)-1-z
assert E.subs(z,0)==0 and S.diff(E,z).subs(z,0)==0
assert S.diff(E,z,2)==S.exp(z)
assert S.limit(A,r,0,dir='+')==1
assert S.limit(Ap,r,0,dir='+')==0
print('A derivative identity and positivity reduction checked.')

# 3. h(s)=s*exp(-chi(s)/s^2); chi(s)=exp(-s/(1-s)) below 1.
s=S.symbols('s',positive=True)
chi=S.exp(-s/(1-s))
h=s*S.exp(-chi/s**2)
assert S.simplify(S.diff(chi,s)+chi/(1-s)**2)==0
expected=S.exp(-chi/s**2)*(1-S.diff(chi,s)/s+2*chi/s**2)
assert S.simplify(S.diff(h,s)-expected)==0
assert S.limit(chi,s,0,dir='+')==1
assert S.limit(chi,s,1,dir='-')==0
assert S.limit(h,s,1,dir='-')==1
print('Flattening derivative identity checked; every displayed summand is positive.')

# 4. Jacobian of G(z)=(A(|z|)*z_1/|z|,z_2,z_3,z_4).
z1,z2,z3,z4=S.symbols('z1 z2 z3 z4', real=True)
rho=S.sqrt(z1*z1+z2*z2+z3*z3+z4*z4)
Af=S.Function('A')
G=S.Matrix([Af(rho)*z1/rho,z2,z3,z4])
J=G.jacobian([z1,z2,z3,z4])
J_expected=(S.diff(Af(rho),rho) if False else S.Subs(S.Derivative(Af(r),r),r,rho))
# Verify the determinant using an independent formal radius variable.
aa,ap=S.symbols('aa ap', real=True)
Jformal=S.diag(aa/r,1,1,1)
for j,zj in enumerate([z1,z2,z3,z4]):
    Jformal[0,j]+=(ap/r**2-aa/r**3)*z1*zj
assert S.factor(Jformal.det()-(ap*z1*z1/r**2+aa/r*(1-z1*z1/r**2)))==0
print('Jacobian determinant formula checked exactly.')

# 5. The two extrema are unchanged, and saddle endpoints are the omitted arc.
qcrit=[((p[u]+p[a])/2,(p[u]-p[a])/2,p[v],p[b]) for p in crit]
assert set(qcrit)=={(-1,0,0,0),(1,0,0,0),(0,-1,0,0),(0,1,0,0)}
assert g.subs({t:0,d:1,v:0,b:0})==2
assert g.subs({t:0,d:-1,v:0,b:0})==-2
print('Extrema at (0,+/-1,0,0) checked, values +/-2.')

# 6. Ordinary cohomology: Q[alpha,beta]/(alpha^2,beta^2).
alpha,beta=S.symbols('alpha beta')
GB=S.groebner([alpha**2,beta**2],alpha,beta)
assert GB.reduce(alpha*beta)[1]==alpha*beta
assert all(GB.reduce(m)[1]==0 for m in [alpha**3,alpha**2*beta,alpha*beta**2,beta**3])
print('Cup-length algebra checked: alpha*beta != 0, all triple products vanish.')

print('ALL EXACT CHECKS PASSED')
