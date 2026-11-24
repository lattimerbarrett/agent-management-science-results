from itertools import product
import sympy as S

# Cohomology ring over F_2, basis 1,a,b,ab.
B=[(0,0),(1,0),(0,1),(1,1)]
def mul(x,y):
    z=[0]*4
    for i,(p,q) in enumerate(B):
        for j,(r,s) in enumerate(B):
            if x[i]*y[j] and p+r<2 and q+s<2:
                z[B.index((p+r,q+s))]^=1
    return tuple(z)
a,b=(0,1,0,0),(0,0,1,0)
zero=(0,0,0,0)
assert mul(a,a)==mul(b,b)==zero
assert mul(a,b)==(0,0,0,1)
positive=[(0,)+x for x in product((0,1),repeat=3)]
assert all(mul(mul(x,y),z)==zero for x,y,z in product(positive,repeat=3))
assert S.gcd(2,2)==2  # minimal Chern number

# The original critical points, and the arc to be merged.
z=S.symbols('z',real=True)
assert S.solve(z*z-1,z)==[-1,1]
theta=S.symbols('theta',real=True)
p=S.Matrix([S.sin(theta),0,S.cos(theta)])
q=S.Matrix([S.sin(theta),0,-S.cos(theta)])
assert S.trigsimp(p.dot(p)-1)==S.trigsimp(q.dot(q)-1)==0
assert S.simplify(p[2]+q[2])==0
assert S.trigsimp(p.diff(theta).dot(p.diff(theta))+q.diff(theta).dot(q.diff(theta)))==2

# Exact endpoint Morse-coordinate identity.
P1,P2,Q1,Q2=S.symbols('P1 P2 Q1 Q2')
u0,v0,s0,t0=P2+P1,P2-P1,Q2+Q1,Q2-Q1
assert S.expand(u0*v0+s0*t0-(P2**2+Q2**2-P1**2-Q1**2))==0

# Capsule formulas: arbitrary smooth A and d.
u,v,s,t,eps=S.symbols('u v s t eps',real=True)
A=S.Function('A')(u); d=S.Function('d')(u)
aa=-eps*A*S.diff(d,u)
bb=1+eps*S.diff(A,u)*S.diff(d,u)
h=A*v+s*t
D=d+v*v+s*s+t*t
coords=(u,v,s,t); Y=(aa,bb*v,s/2,t/2)
Yh=sum(c*S.diff(h,x) for c,x in zip(Y,coords))
YD=sum(c*S.diff(D,x) for c,x in zip(Y,coords))
assert S.simplify(Yh-h)==0
assert S.simplify(YD-(-eps*A*S.diff(d,u)**2+2*bb*v*v+s*s+t*t))==0

# Flat radial replacement and its logarithmic derivative.
r=S.symbols('r',positive=True)
chi=S.Function('chi')(r)
psi=r*S.exp(-chi/r**2)
assert S.simplify(S.diff(psi,r)/psi-(1/r-S.diff(chi,r)/r**2+2*chi/r**3))==0
flat=r*S.exp(-1/r**2)
for k in range(9):
    assert S.limit(S.diff(flat,r,k),r,0,dir='+')==0

# Exact finite-sample variance identity (the integral version is identical).
for n in range(2,7):
    xs=S.symbols('x:'+str(n)); mean=sum(xs)/n
    assert S.expand(sum((x-mean)**2 for x in xs)-sum((x-y)**2 for x in xs for y in xs)/(2*n))==0

# Fourier-mode calculation behind Wirtinger's inequality.
tau=S.symbols('tau',real=True)
for k in range(1,5):
    f=S.cos(k*tau)
    assert S.integrate(S.diff(f,tau)**2-k*k*f*f,(tau,0,2*S.pi))==0

print('All exact algebraic and symbolic checks passed.')
