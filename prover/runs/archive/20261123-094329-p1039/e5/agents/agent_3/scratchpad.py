import sympy as s
from pathlib import Path
x,y,a,b,c=s.symbols('x y eta eta_prime eta_second', real=True)
# Worm tangential Levi numerator on rho=0, xi=x+iy and |xi-1|^2=1-eta.
L=b*b-2*b*y+(2*x+c)*(1-a)
SOS=(b-y)**2+(x-a)**2+a*(1-a)+c*(1-a)
boundary=(x-1)**2+y*y-(1-a)
assert s.expand(L-SOS+boundary)==0
# Direct tangential form before using boundary:
u=s.symbols('u', real=True)
raw=(b-2*y)**2+2*(b-2*y)*y+(2*x+c)*u
assert s.expand(raw.subs(u,1-a)-L)==0
result='''For the standard C^2 worm defining function rho=|z-exp(i log|w|^2)|^2-1+eta(log|w|^2), the tangential Levi form (times |w|^2, in the tangent vector (rho_w,-rho_z)) is
eta_prime^2-2 eta_prime*y+(2*x+eta_second)*(1-eta).
On the boundary (x-1)^2+y^2=1-eta, this equals
(eta_prime-y)^2+(x-eta)^2+eta*(1-eta)+eta_second*(1-eta).
Thus it is nonnegative when 0<=eta<=1 and eta_second>=0.
SymPy verified both identities exactly.
'''
# All dimensions: Cauchy-Schwarz reduction for rho_n=rho_2+||zeta||^2.
N=(b-y)**2+(x-1)**2+(2*x+c-1)*(1-a)
assert s.expand(N-SOS)==0
ar,ai,br,bi=s.symbols('ar ai br bi', real=True)
A=ar+s.I*ai
B=br+s.I*bi
cross=s.expand(2*s.re(s.I*A*s.conjugate(B)))
assert s.expand(s.expand_complex(abs(A-s.I*B)**2)-abs(A)**2-abs(B)**2-cross)==0
result+='''\nALL DIMENSIONS: Add ||zeta||^2 to rho. For a=e^{-it}v_z, b=v_w/w, c=v_zeta, tangent vectors satisfy
(bar(xi)-1)*a + bar(zeta).c = -(eta_prime-2*y)*b.
The Levi form equals |a-i*b|^2+||c||^2+(2*x+eta_second-1)*|b|^2.
Cauchy-Schwarz and |xi-1|^2+||zeta||^2=1-eta imply
(1-eta)*Levi >= N*|b|^2,
N=(eta_prime-y)^2+(x-eta)^2+eta*(1-eta)+eta_second*(1-eta)>=0.
At eta=1 tangency forces b=0 because eta_prime!=0, so Levi>=0 too.
SymPy verified the completed-square and N identities exactly.
'''
# Independent Wirtinger differentiation from the real defining function at w=1.
p,q=s.symbols('p q', real=True)
t=s.log(p*p+q*q)
eta=s.Function('eta')
rho=x*x+y*y-2*(x*s.cos(t)+y*s.sin(t))+eta(t)
def dz(expr): return (s.diff(expr,x)-s.I*s.diff(expr,y))/2
def dzbar(expr): return (s.diff(expr,x)+s.I*s.diff(expr,y))/2
def dw(expr): return (s.diff(expr,p)-s.I*s.diff(expr,q))/2
def dwbar(expr): return (s.diff(expr,p)+s.I*s.diff(expr,q))/2
def at1(expr):
    return s.simplify(expr.subs({p:1,q:0}).doit())
assert s.simplify(at1(dz(rho))-(x-s.I*y-1))==0
assert s.simplify(at1(dw(rho))-(-2*y+s.Subs(s.Derivative(eta(s.Symbol('_t')),s.Symbol('_t')),s.Symbol('_t'),0)))==0
assert at1(dzbar(dz(rho)))==1
assert at1(dwbar(dz(rho)))==s.I
rww=at1(dwbar(dw(rho)))
assert s.simplify(rww-2*x-s.Subs(s.Derivative(eta(s.Symbol('_t')),(s.Symbol('_t'),2)),s.Symbol('_t'),0))==0
result+='\nIndependent real-coordinate Wirtinger differentiation verified rho_z, rho_w, rho_zbarz, rho_zbarw and rho_wbarw at w=1 exactly.\n'
Path('workspace/agent3_worm_levi.txt').write_text(result)
Path('workspace/agent3_worm_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent3_worm_proof.md').write_text(r'''# Verified generalized-worm geometry (not an Oka obstruction)

Fix mu>0. Let h(s)=0 for s<=0 and h(s)=integral_0^s exp(-1/u)du for s>0, and put eta(t)=h(t-mu)+h(-t-mu). Then eta is smooth, convex and nonnegative, eta=0 exactly on [-mu,mu], eta tends to infinity at both ends, and eta' is nonzero where eta=1. Smoothness follows because exp(-1/s) and every derivative tend to zero at 0+. For s>0, h'=exp(-1/s)>0 and h''=exp(-1/s)/s^2>0.

In C^n with coordinates (z,w,zeta), w!=0, define
rho=|z-exp(i t)|^2+||zeta||^2-1+eta(t), t=log|w|^2.
Let Omega={rho<0} and K={rho<=0}. Its projection to w is the annulus eta(log|w|^2)<1; each fiber is a ball in C^(n-1) of radius sqrt(1-eta), centered at (exp(i t),0). The base and fibers are connected, and the centers give a continuous section, proving connectedness. The base is bounded and bounded away from w=0; the fiber radius is at most 1 and its center has norm 1. Thus Omega is bounded, nonempty, and its closure lies in w!=0.

Boundary regularity: if rho_z and all rho_zeta vanish, then z=exp(i t), zeta=0. On rho=0 this gives eta(t)=1. At such a point rho_w=eta'(t)/w !=0. Thus d rho!=0 everywhere on rho=0. Therefore K=closure(Omega) has smooth boundary and belongs to K_n.

For Levi positivity put xi=z exp(-i t)=x+i y, A=exp(-i t)v_z, B=v_w/w and C=v_zeta. Write d=eta'-2y. Tangency means (bar(xi)-1)A+bar(zeta).C=-d B. The Levi form is
L=|A-i B|^2+||C||^2+(2x+eta''-1)|B|^2.
The vector ell=(bar(xi)-1,bar(zeta)) has norm squared R=1-eta on the boundary. For U=(A-i B,C), tangency gives ell.U=-(eta'-y+i(x-1))B. If R>0, Cauchy-Schwarz gives
R L >= N |B|^2,
N=(eta'-y)^2+(x-eta)^2+eta(1-eta)+eta''(1-eta)>=0.
If B=0 directly L=|A|^2+||C||^2>=0. If R=0, then xi=1,zeta=0, eta=1, and eta'!=0 forces B=0 by tangency. Thus all boundary Levi forms are nonnegative in the stated orientation.

The boundary is strictly pseudoconvex except on A={z=0,zeta=0, |log|w|^2|<=mu}. Indeed N>0 for 0<eta<1, eta=1 was handled separately, and when eta=0 its derivatives vanish and N=|xi|^2. Vanishing N then implies xi=0 and zeta=0. At A the Levi null space is exactly the w-direction.

For mu>pi, one can prove failure of a Stein neighborhood basis directly (agent4's moving-annulus argument). Let r=exp(-pi/2), R=exp(pi/2). Both boundary circles at w-moduli r,R have t=+-pi and hence fiber center exp(i t)=-1. Thus for every z in D(-1,1), both circles (z,w,0) lie in Omega. Meanwhile the full compact annulus A_0={(0,w,0):r<=|w|<=R} lies in K, since eta=0 and rho=0 there. Every neighborhood U of K therefore contains A_z for z sufficiently close to 0. Choose a negative real such z_0 in D(-1,1), and move z continuously along the segment to -1/2. The boundaries of all A_z remain in K, while the entire moving family remains in a fixed compact ambient set. If U is Stein, take a proper continuous psh exhaustion phi of U. Its supremum on K is finite. On every A_z already contained in U, the subharmonic maximum principle bounds phi by this same supremum. The set of parameters for which A_z is contained in U is open and closed: closedness follows because all A_z then lie in a single compact sublevel of phi. Hence the endpoint annulus also lies in U. In particular p=(-1/2,1,0) belongs to every Stein neighborhood U of K. But rho(p)=|-1/2-1|^2-1=5/4>0, so p is outside K. This proves that K has no Stein neighborhood basis, in every dimension.

IMPORTANT: No assertion that these complements are non-Oka has been established here. The missing bridge cannot be inferred from these Levi computations.
''')
print(result)
