from pathlib import Path
import sympy as s
n,r2=s.symbols('n r2', positive=True)
x,y,t=s.symbols('x y t', real=True)
# Formal radial Laplacian in d=n-1 variables acting on F(r^2).
def lap_rad(F):return 4*r2*s.diff(F,r2,2)+2*(n-1)*s.diff(F,r2)
W=(1+r2)**(-(n-2))
identity=s.simplify(lap_rad(W)-2*(n-2)*(n-1)*(r2-1)*(1+r2)**(-n))
assert identity==0
# Geometry: h=P_L*f(r^2), P_L harmonic homogeneous degree L.
L,j=s.symbols('L j', integer=True, nonnegative=True)
a=s.symbols('a0:4')
f=sum(a[k]*r2**k for k in range(4))
delta_coefficient=4*r2*s.diff(f,r2,2)+2*(n-1+2*L)*s.diff(f,r2)
euler_coefficient=L*f+2*r2*s.diff(f,r2)
source=s.expand(f-euler_coefficient+(1+r2)*delta_coefficient/(2*(n-1)))
# Linear h and special sphere tangent graph r² yield constant/gauge source.
assert s.simplify(source.subs({L:1,a[0]:1,a[1]:0,a[2]:0,a[3]:0}))==0
assert s.simplify(source.subs({L:0,a[0]:0,a[1]:1,a[2]:0,a[3]:0}))==1
# Harmonic homogeneous h=P_L gives coefficient 1-L.
assert s.simplify(source.subs({a[0]:1,a[1]:0,a[2]:0,a[3]:0})-(1-L))==0
# Check hyperspherical ODE hypergeometric parameters through coefficient equation.
z=s.symbols('z', positive=True)
aH=(L-1)/2;bH=(L+n)/2;cH=L+n/2
# y=sin(theta)^L F(sin²theta); expected ODE F coefficient.
F=s.Function('F')
ytheta=lambda v:None
th=s.symbols('theta', positive=True)
y=s.sin(th)**L*F(s.sin(th)**2)
ode=s.diff(y,th,2)+(n-1)*s.cot(th)*s.diff(y,th)+(n-L*(L+n-2)/s.sin(th)**2)*y
# Verify after choosing symbolic F polynomial of degree≤3 (sufficient for order2 operator).
for q in range(4):
    Y=s.sin(th)**(L+2*q)
    left=s.diff(Y,th,2)+(n-1)*s.cot(th)*s.diff(Y,th)+(n-L*(L+n-2)/s.sin(th)**2)*Y
    target=4*s.sin(th)**L*(s.sin(th)**2*(1-s.sin(th)**2)*q*(q-1)*s.sin(th)**(2*max(q-2,0))+(cH-(aH+bH+1)*s.sin(th)**2)*q*s.sin(th)**(2*max(q-1,0))-aH*bH*s.sin(th)**(2*q))
    check=s.trigsimp(s.powsimp(s.expand_trig((left-target)/s.sin(th)**L),force=True))
    if check!=0:
        for nn in range(3,21):
            for ll in range(2,9):
                assert s.trigsimp((left-target).subs({n:nn,L:ll}))==0
# DtoN cancellation n=18,l=k+2.
k=s.symbols('k', integer=True, nonnegative=True)
D18=s.prod(k+2*q+1 for q in range(10))/s.prod(k+2*q for q in range(1,10))
for kval in range(12):
    Dgamma=2*s.gamma((kval+2)/2)*s.gamma(s.Rational(kval+21,2))/(s.gamma(s.Rational(kval+1,2))*s.gamma(s.Rational(kval+20,2)))
    assert abs(float(D18.subs(k,kval))-float(Dgamma))<1e-10
print('PASS radial shape-variation identity, source and gauge formulas, hypergeometric ODE, n18 DtN checks')
if Path(__file__).name=='scratchpad.py':
    Path('workspace/agent4_source_checks.py').write_text(Path(__file__).read_text())
print('Polynomial source/P_L =',s.collect(source,a))
